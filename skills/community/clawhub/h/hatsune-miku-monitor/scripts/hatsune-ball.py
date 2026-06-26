#!/usr/bin/env python3
"""
初音未来悬浮球 v6 - 性能优化版
- 后台线程处理数据，避免阻塞 UI
- 简化 GIF 处理，提升流畅度
- 点击切换状态面板
- 贴边自动隐藏
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import psutil
import time
import os
import threading

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class HatsuneBall(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)

        self.set_title("初音未来")
        self.set_keep_above(True)
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_app_paintable(True)

        screen = Gdk.Screen.get_default()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)

        self.current_opacity = 0.95
        self.set_opacity(self.current_opacity)

        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        if monitor:
            geo = monitor.get_geometry()
            self.screen_w, self.screen_h = geo.width, geo.height
        else:
            self.screen_w, self.screen_h = 1920, 1080

        self.move(self.screen_w - 150, self.screen_h // 2 - 100)

        # 状态
        self._dragging = False
        self._drag_offset = (0, 0)
        self._drag_start = (0, 0)
        self._panel_visible = False
        self._edge_hidden = False
        self._edge_type = None
        self._last_x = 0
        self._last_y = 0

        # 数据缓存（后台更新）
        self._data = {
            'cpu': 0,
            'mem': 0,
            'disk': 0,
            'temp': None
        }

        # GIF
        self.gif_frames = []
        self.gif_index = 0

        self._build_ui()
        self._bind_events()

        # 后台数据线程
        self._running = True
        threading.Thread(target=self._data_worker, daemon=True).start()

        # 定时器（只更新 UI，不阻塞）
        GLib.timeout_add(1000, self._update_ui)
        GLib.timeout_add(100, self._check_edge)
        GLib.timeout_add(100, self._animate_gif)

    def _build_ui(self):
        outer = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.add(outer)

        self.img_widget = Gtk.Image.new()
        self._load_image()
        outer.pack_start(self.img_widget, False, False, 0)

        self.panel = Gtk.Box.new(Gtk.Orientation.VERTICAL, 4)
        self.panel.set_margin_start(8)
        self.panel.set_margin_end(8)
        self.panel.set_margin_top(6)
        self.panel.set_margin_bottom(6)
        self.panel.set_name("panel")

        self.cpu_lbl  = self._make_label("CPU:  --%",  "#00ff00")
        self.mem_lbl  = self._make_label("内存: --%",  "#00ffff")
        self.disk_lbl = self._make_label("磁盘: --%",  "#ff9900")
        self.temp_lbl = self._make_label("温度: --°C", "#ff6666")
        
        for lbl in [self.cpu_lbl, self.mem_lbl, self.disk_lbl, self.temp_lbl]:
            self.panel.pack_start(lbl, False, False, 0)

        self.panel.pack_start(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), False, False, 2)

        alpha_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
        alpha_lbl = Gtk.Label()
        alpha_lbl.set_markup("<span foreground='#aaaaaa' size='small'>透明度</span>")
        alpha_box.pack_start(alpha_lbl, False, False, 0)

        self.alpha_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.2, 1.0, 0.05)
        self.alpha_scale.set_value(self.current_opacity)
        self.alpha_scale.set_draw_value(False)
        self.alpha_scale.set_hexpand(True)
        self.alpha_scale.connect("value-changed", self._on_alpha_changed)
        alpha_box.pack_start(self.alpha_scale, True, True, 0)
        self.panel.pack_start(alpha_box, False, False, 0)

        # 一键加速按钮
        boost_btn = Gtk.Button.new_with_label("⚡ 一键加速")
        boost_btn.set_name("boost-btn")
        boost_btn.connect("clicked", self._on_boost)
        self.panel.pack_start(boost_btn, False, False, 2)

        close_btn = Gtk.Button.new_with_label("✕ 关闭")
        close_btn.set_name("close-btn")
        close_btn.connect("clicked", self._on_close)
        self.panel.pack_start(close_btn, False, False, 2)

        outer.pack_start(self.panel, False, False, 0)
        self.panel.hide()

        css = Gtk.CssProvider()
        css.load_from_data(b"""
            #panel {
                background-color: rgba(20, 20, 40, 0.95);
                border-radius: 12px;
                border: 1px solid #334466;
            }
            #boost-btn {
                background: rgba(50,200,50,0.3);
                color: #00ff00;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            #boost-btn:hover {
                background: rgba(50,200,50,0.7);
            }
            #close-btn {
                background: rgba(255,50,50,0.3);
                color: white;
                border: none;
                border-radius: 6px;
            }
            #close-btn:hover {
                background: rgba(255,50,50,0.7);
            }
        """)
        for w in [self.panel, boost_btn, close_btn]:
            w.get_style_context().add_provider(css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _load_image(self):
        """快速 GIF 加载，不去背景"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(script_dir)
        
        gif_paths = [
            os.path.join(skill_dir, "assets", "chuyin.gif"),
            "/tmp/chuyin.gif",
        ]
        
        if HAS_PIL:
            for path in gif_paths:
                if os.path.exists(path):
                    try:
                        print(f"📹 加载: {path}")
                        img = Image.open(path)
                        frames = []
                        idx = 0
                        while True:
                            try:
                                img.seek(idx)
                                frame = img.convert("RGBA")
                                frame = frame.resize((120, 120), Image.Resampling.LANCZOS)
                                data = frame.tobytes()
                                w, h = frame.size
                                pb = GdkPixbuf.Pixbuf.new_from_data(
                                    data, GdkPixbuf.Colorspace.RGB, True, 8, w, h, w * 4
                                ).copy()
                                frames.append(pb)
                                idx += 1
                            except EOFError:
                                break
                        
                        if frames:
                            self.gif_frames = frames
                            self.img_widget.set_from_pixbuf(frames[0])
                            print(f"✅ {len(frames)} 帧")
                            return
                    except Exception as e:
                        print(f"⚠️ {e}")
        
        self.img_widget.set_from_icon_name("face-smile-symbolic", Gtk.IconSize.DIALOG)

    def _animate_gif(self):
        if self.gif_frames:
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            self.img_widget.set_from_pixbuf(self.gif_frames[self.gif_index])
        return True

    def _make_label(self, text, color):
        lbl = Gtk.Label()
        lbl.set_markup(f'<span foreground="{color}" size="small">{text}</span>')
        lbl.set_halign(Gtk.Align.START)
        return lbl

    def _bind_events(self):
        self.connect("button-press-event",   self._on_press)
        self.connect("button-release-event", self._on_release)
        self.connect("motion-notify-event",  self._on_motion)

    def _on_press(self, w, e):
        if e.button == 1:
            self._drag_start = (e.x_root, e.y_root)
            self._dragging = True
            self._drag_offset = (e.x, e.y)

    def _on_release(self, w, e):
        if self._dragging:
            dx = abs(e.x_root - self._drag_start[0])
            dy = abs(e.y_root - self._drag_start[1])
            
            if dx < 5 and dy < 5:
                self._toggle_panel()
            
            self._dragging = False
            GLib.timeout_add(100, self._check_edge_once)

    def _on_motion(self, w, e):
        if self._dragging:
            nx = int(e.x_root - self._drag_offset[0])
            ny = int(e.y_root - self._drag_offset[1])
            self.move(nx, ny)
            self._last_x, self._last_y = nx, ny

    def _toggle_panel(self):
        if self._panel_visible:
            self.panel.hide()
            self._panel_visible = False
        else:
            self.panel.show_all()
            self._panel_visible = True

    def _check_edge_once(self):
        self._check_edge()
        return False

    def _check_edge(self):
        if self._dragging:
            return True
        
        x, y = self.get_position()
        w, h = self.get_size()
        
        threshold = 50
        
        at_left   = x < threshold
        at_right  = x + w > self.screen_w - threshold
        at_top    = y < threshold
        at_bottom = y + h > self.screen_h - threshold
        
        if at_left or at_right or at_top or at_bottom:
            if not self._edge_hidden:
                if at_left:
                    self._hide_to_edge("left", x, y)
                elif at_right:
                    self._hide_to_edge("right", x, y)
                elif at_top:
                    self._hide_to_edge("top", x, y)
                elif at_bottom:
                    self._hide_to_edge("bottom", x, y)
        else:
            if self._edge_hidden:
                self._show_from_edge()
        
        return True

    def _hide_to_edge(self, edge, x, y):
        self._edge_hidden = True
        self._edge_type = edge
        self._last_x, self._last_y = x, y
        
        if edge == "left":
            self.move(-110, y)
        elif edge == "right":
            self.move(self.screen_w - 10, y)
        elif edge == "top":
            self.move(x, -110)
        elif edge == "bottom":
            self.move(x, self.screen_h - 10)

    def _show_from_edge(self):
        if not self._edge_hidden:
            return
        
        if self._edge_type == "left":
            self.move(0, self._last_y)
        elif self._edge_type == "right":
            self.move(self.screen_w - 140, self._last_y)
        elif self._edge_type == "top":
            self.move(self._last_x, 0)
        elif self._edge_type == "bottom":
            self.move(self._last_x, self.screen_h - 140)
        
        self._edge_hidden = False

    def _on_alpha_changed(self, scale):
        val = scale.get_value()
        self.set_opacity(val)
        self.current_opacity = val

    def _on_close(self, btn):
        self._running = False
        Gtk.main_quit()

    def _on_boost(self, btn):
        """一键加速：清理内存缓存"""
        # 记录清理前内存
        mem_before = psutil.virtual_memory()
        self._boost_mem_before = mem_before.used / 1024 / 1024 / 1024  # GB
        
        threading.Thread(target=self._boost_worker, daemon=True).start()
        
        # UI 反馈
        btn.set_label("⚡ 加速中...")
        btn.set_sensitive(False)
        GLib.timeout_add(3000, lambda: self._boost_done(btn))

    def _boost_worker(self):
        """后台执行清理 - 增强版"""
        import subprocess
        import gc
        
        # 1. Python 垃圾回收（多次）
        for _ in range(3):
            gc.collect()
        
        # 2. 清理浏览器缓存（如果有）
        try:
            subprocess.run(['pkill', '-f', 'chrome.*--type=renderer'], 
                          check=False, stderr=subprocess.DEVNULL)
        except:
            pass
        
        # 3. sync 写入磁盘
        try:
            subprocess.run(['sync'], check=False)
        except:
            pass
        
        # 4. 清理系统缓存（3种级别）
        # 1 = PageCache, 2 = dentries+inodes, 3 = 全部
        for cache_level in [1, 2, 3]:
            try:
                # 尝试无密码 sudo（可能需要配置 sudoers）
                subprocess.run(
                    ['sudo', '-n', 'sh', '-c', f'echo {cache_level} > /proc/sys/vm/drop_caches'],
                    check=False, stderr=subprocess.DEVNULL, timeout=1
                )
            except:
                pass
        
        # 5. 清理 swap（如果有）
        try:
            subprocess.run(['sudo', '-n', 'swapoff', '-a'], 
                          check=False, stderr=subprocess.DEVNULL, timeout=2)
            subprocess.run(['sudo', '-n', 'swapon', '-a'], 
                          check=False, stderr=subprocess.DEVNULL, timeout=2)
        except:
            pass
        
        # 6. 清理 journalctl 日志
        try:
            subprocess.run(['sudo', '-n', 'journalctl', '--vacuum-time=1d'], 
                          check=False, stderr=subprocess.DEVNULL, timeout=3)
        except:
            pass
        
        # 7. 清理用户缓存目录
        import shutil
        cache_dirs = [
            os.path.expanduser('~/.cache/thumbnails'),
            os.path.expanduser('~/.cache/pip'),
            os.path.expanduser('~/.cache/mesa_shader_cache'),
        ]
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    shutil.rmtree(cache_dir, ignore_errors=True)
                    os.makedirs(cache_dir, exist_ok=True)
                except:
                    pass

    def _boost_done(self, btn):
        """加速完成，显示效果"""
        # 计算清理的内存
        mem_after = psutil.virtual_memory()
        mem_after_gb = mem_after.used / 1024 / 1024 / 1024
        freed = self._boost_mem_before - mem_after_gb
        
        if freed > 0.01:  # 释放超过 10MB
            btn.set_label(f"✅ 释放 {freed:.2f}GB")
        else:
            btn.set_label("✅ 加速完成")
        
        btn.set_sensitive(True)
        # 3秒后恢复原始文字
        GLib.timeout_add(3000, lambda: self._restore_boost_btn(btn))
        return False
    
    def _restore_boost_btn(self, btn):
        """恢复按钮文字"""
        btn.set_label("⚡ 一键加速")
        return False

    def _data_worker(self):
        """后台线程：不阻塞 UI"""
        while self._running:
            try:
                # 非阻塞版本
                self._data['cpu'] = psutil.cpu_percent(interval=0)
                mem = psutil.virtual_memory()
                self._data['mem'] = mem.percent
                disk = psutil.disk_usage('/')
                self._data['disk'] = disk.percent
                
                # 温度
                try:
                    temps = psutil.sensors_temperatures()
                    if temps:
                        for name, entries in temps.items():
                            for e in entries:
                                if 'cpu' in e.label.lower() or 'core' in e.label.lower():
                                    self._data['temp'] = e.current
                                    break
                            if self._data['temp']:
                                break
                except:
                    pass
            except:
                pass
            
            time.sleep(2)

    def _update_ui(self):
        """只更新 UI，不阻塞"""
        try:
            self.cpu_lbl.set_markup(f'<span foreground="#00ff00" size="small">CPU:  {self._data["cpu"]}%</span>')
            self.mem_lbl.set_markup(f'<span foreground="#00ffff" size="small">内存: {self._data["mem"]}%</span>')
            self.disk_lbl.set_markup(f'<span foreground="#ff9900" size="small">磁盘: {self._data["disk"]}%</span>')
            
            if self._data['temp']:
                self.temp_lbl.set_markup(f'<span foreground="#ff6666" size="small">温度: {self._data["temp"]:.0f}°C</span>')
            else:
                self.temp_lbl.set_markup('<span foreground="#ff6666" size="small">温度: N/A</span>')
        except:
            pass
        return True


if __name__ == "__main__":
    print("🎤 初音未来悬浮球 v6 - 性能优化版")
    
    win = HatsuneBall()
    win.connect("destroy", lambda _: win._on_close(None))
    win.show_all()
    win.get_child().get_children()[-1].hide()
    Gtk.main()
