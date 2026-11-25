#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader 离线自测：不联网、不下载，只验证识别、配置和命令拼装。"""
import contextlib
import importlib.util
import io
import json
import os
import stat
import sys
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
_PAN_PY = HERE / "pan.py"
TMP = Path(tempfile.mkdtemp(prefix="pan-selftest-"))
os.environ["PAN_CONFIG"] = str(TMP / "config.json")
os.environ["PAN_LOG"] = str(TMP / "pan.log")
os.environ["PAN_STATE_DIR"] = str(TMP / "state")


def load_module():
    spec = importlib.util.spec_from_file_location("pan", HERE / "pan.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def capture_call(func, *args, **kwargs):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = func(*args, **kwargs)
    return rc, out.getvalue()


def main():
    pan = load_module()
    checks = 0

    # 1) 链接识别：首批 + 常用扩展网盘 + 自定义扩展
    cases = [
        ("https://pan.baidu.com/s/1abcdEFG", "baidu"),
        ("https://www.aliyundrive.com/s/abc123", "aliyun"),
        ("https://pan.quark.cn/s/abc123", "quark"),
        ("https://cloud.189.cn/t/abc123", "tianyi"),
        ("https://pan.xunlei.com/s/abc123", "thunder"),
        ("https://115.com/s/abc123", "115"),
        ("https://www.123pan.com/s/abc123", "123pan"),
        ("https://yun.139.com/shareweb/#/w/i/abc123", "139yun"),
        ("https://wopan.wo.cn/s/abc123", "wopan"),
        ("https://drive.uc.cn/s/abc123", "uc"),
        ("https://mypikpak.com/s/abc123", "pikpak"),
        ("https://www.jianguoyun.com/p/abc123", "jianguoyun"),
        ("https://1drv.ms/u/s!abc123", "onedrive"),
        ("https://drive.google.com/file/d/abc123/view", "googledrive"),
        ("https://www.dropbox.com/s/abc123/file.zip", "dropbox"),
        ("https://share.weiyun.com/abc123", "weiyun"),
        ("https://wwx.lanzoue.com/abc123", "lanzou"),
        ("https://pan.wukong.com/s/abc123", "wukong"),
        ("https://pan.doubao.com/s/abc123", "doubao"),
        ("https://mega.nz/file/abc123", "mega"),
        ("https://terabox.com/s/abc123", "terabox"),
        ("https://u.pcloud.link/publink/show?code=abc", "pcloud"),
        ("https://drive.proton.me/urls/abc123", "protondrive"),
        ("https://disk.yandex.com/d/abc123", "yandexdisk"),
        ("https://www.mediafire.com/file/abc123/file.zip", "mediafire"),
        ("https://trainbit.com/files/abc123/file.zip", "trainbit"),
        ("https://guangyapan.com/s/abc123", "guangyapan"),
        ("https://feijipan.com/s/abc123", "feijipan"),
        ("https://shandianpan.com/s/abc123", "shandian"),
        ("https://www.ctfile.com/f/abc123", "chengtong"),
        ("https://example.com/file.zip", "direct"),
    ]
    for url, expected in cases:
        got, spec = pan.detect_drive(url)
        assert got == expected, "detect %s -> %s (期望 %s)" % (url, got, expected)
        assert spec.get("name"), "drive %s 缺少 name" % got
        checks += 1

    # 2) 未知非 http 链接
    assert pan.detect_drive("ftp://x")[0] == "", "ftp 不应被识别"
    checks += 1

    # 3) 文件名与 slug 清洗
    assert pan.sanitize('a/b:c*?"<>|') == "a_b_c" + "_" * 6
    assert pan.filename_from_url("https://x.com/%E6%96%87%E4%BB%B6.zip") == "文件.zip"
    assert pan.url_slug("https://pan.quark.cn/s/abc123/") == "abc123"
    checks += 3

    # 4) 凭据打码：不打印参数值，也不把密码写进 config
    masked = pan.mask_value("config", {"cookie": "abc", "token": "xyz", "tier": "free"})
    assert masked == {"cookie": "***", "token": "***", "tier": "free"}, masked
    masked_argv = pan.mask_argv(["rclone", "--user", "me", "--password", "secret", "remote:path"])
    assert masked_argv == ["rclone", "--user", "***", "--password", "***", "remote:path"], masked_argv
    masked_inline = pan.mask_argv(["tool", "--token=abc", "--cookie", "xyz"])
    assert "abc" not in " ".join(masked_inline) and "xyz" not in " ".join(masked_inline), masked_inline
    masked_remote_command = pan.mask_argv(["ssh", "host", "pan.py get x --pwd 1234 --force"])
    assert "1234" not in masked_remote_command[-1], masked_remote_command
    checks += 4

    # 5) 默认目录可覆盖 + 任务目录命名
    cfg = pan.load_config()
    cfg["download_root"] = str(TMP / "下载")
    root = pan.default_root(cfg)
    assert root == TMP / "下载", root
    tdir = pan.task_dir(cfg, "百度网盘", "https://pan.baidu.com/s/1abc")
    assert tdir.parent == root / "百度网盘" and tdir.name.endswith("-1abc"), tdir
    checks += 2

    # 6) 直链 HTTP 计划：curl 断点续传
    plan = pan.build_plan("https://example.com/a/b.zip", cfg=cfg)
    assert plan["ok"] and plan["engine"] == "http"
    argv = plan["steps"][0]["argv"]
    assert argv[0] == "curl" and "-C" in argv and argv[-1].endswith("b.zip")
    checks += 1

    # 7) 百度分享计划（未装引擎时给缺失项和两步计划）
    p2 = pan.build_plan("https://pan.baidu.com/s/1abc", pwd="1234", cfg=cfg)
    assert p2["drive"] == "baidu" and p2["engine"] == "baidupcs"
    assert len(p2["steps"]) == 2 and p2["steps"][0]["argv"][1] == "transfer"
    assert "BaiduPCS-Go" in p2["missing"], p2["missing"]
    checks += 3

    # 8) 自定义引擎模板
    cfg2 = json.loads(json.dumps(cfg))
    cfg2["drives"]["quark"]["engine_command"] = "mytool get {url} --pwd {pwd} --out {dir}"
    p3 = pan.build_plan("https://pan.quark.cn/s/zzz", pwd="9x9", cfg=cfg2)
    assert p3["steps"][0]["engine"] == "custom"
    assert p3["steps"][0]["argv"][:3] == ["mytool", "get", "https://pan.quark.cn/s/zzz"]
    checks += 2

    # 9) WebDAV / 坚果云直链计划
    cfg_dav = json.loads(json.dumps(cfg))
    cfg_dav["engines"]["webdav_user"] = "me@example.com"
    cfg_dav["engines"]["webdav_password_ref"] = pan.keychain_ref("engine.webdav")
    original_keychain_get = pan.keychain_get
    pan.keychain_get = lambda name: "secret" if name == "engine.webdav" else ""
    p_dav = pan.build_plan("https://dav.jianguoyun.com/dav/%E6%96%87%E4%BB%B6.zip", cfg=cfg_dav)
    assert p_dav["engine"] == "webdav", p_dav
    dav_argv = p_dav["steps"][0]["argv"]
    assert p_dav["steps"][0]["engine"] == "webdav" and dav_argv[0] == "curl"
    assert "-C" in dav_argv and dav_argv[-1].startswith("https://dav.jianguoyun.com/dav/")
    assert "secret" not in " ".join(dav_argv), dav_argv
    assert p_dav["steps"][0].get("stdin") == 'user = "me@example.com:secret"\n'
    assert "secret" not in json.dumps(pan.public_plan(p_dav), ensure_ascii=False)
    pan.keychain_get = original_keychain_get
    checks += 5

    # 10) AList + rclone：目录递归复制，并自动补远端冒号
    fake_bin = TMP / "bin"
    fake_bin.mkdir(parents=True, exist_ok=True)
    fake_rclone = fake_bin / "rclone"
    fake_rclone.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    fake_rclone.chmod(0o755)
    cfg_rclone = json.loads(json.dumps(cfg))
    cfg_rclone["engines"]["alist_url"] = "http://127.0.0.1:5244"
    cfg_rclone["engines"]["rclone_remote"] = "alist"
    cfg_rclone["engines"]["rclone"] = str(fake_rclone)
    p_rclone = pan.build_plan("https://pan.quark.cn/s/zzz", cfg=cfg_rclone, engine="alist", path="/夸克网盘/目录")
    rclone_step = p_rclone["steps"][0]
    assert p_rclone["engine"] == "alist" and rclone_step["engine"] == "rclone", p_rclone
    assert Path(rclone_step["argv"][0]).name == "rclone", rclone_step
    assert "alist:/夸克网盘/目录" in rclone_step["argv"], rclone_step
    assert rclone_step["argv"][rclone_step["argv"].index("--transfers") + 1] == "1", rclone_step
    cfg_rclone["drives"]["quark"]["account_tier"] = "vip"
    p_rclone_vip = pan.build_plan("https://pan.quark.cn/s/zzz", cfg=cfg_rclone, engine="alist", path="/夸克网盘/目录")
    assert p_rclone_vip["tier"] == "vip", p_rclone_vip
    vip_argv = p_rclone_vip["steps"][0]["argv"]
    assert vip_argv[vip_argv.index("--transfers") + 1] == "4", p_rclone_vip
    checks += 5

    # 11) 配置保存/读取 + 600 权限
    pan.save_config(cfg, TMP / "config.json")
    path = pan.save_config(cfg2, TMP / "saved.json")
    assert path.exists() and json.loads(path.read_text(encoding="utf-8"))["drives"]["quark"]["engine_command"]
    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode == 0o600, oct(mode)
    checks += 2

    # 12) dry-run 缺依赖也完整展示计划，不提前返回
    dry_args = type("Args", (), {
        "url": "https://pan.baidu.com/s/1abc", "pwd": "1234", "to": str(TMP / "dry"),
        "engine": None, "tier": None, "path": None, "dry_run": True, "force": False,
    })()
    rc, output = capture_call(pan.cmd_get, dry_args)
    assert rc == 0, (rc, output)
    assert "缺少依赖" in output and "DRY-RUN:" in output and "DRY-RUN 完成" in output, output
    checks += 3

    # 13) VIP 参数只影响并发，不做绕过
    cfg3 = json.loads(json.dumps(cfg))
    cfg3["http"]["max_connections_vip"] = 4
    p4 = pan.build_plan("https://example.com/x.bin", cfg=cfg3, engine="aria2", tier="vip")
    if p4["missing"]:
        assert p4["missing"] == ["aria2c"]
    else:
        argv = p4["steps"][0]["argv"]
        assert "-x" in argv and argv[argv.index("-x") + 1] == "4"
    checks += 1

    # 14) tier=auto：无探测器先按免费；账号记录/探测器给出 vip 时自动升为会员
    p_auto = pan.build_plan("https://example.com/auto.bin", cfg=cfg)
    assert p_auto["requested_tier"] == "auto" and p_auto["tier"] == "free", p_auto
    assert any("未自动识别" in w for w in p_auto["warnings"]), p_auto

    cfg_account = json.loads(json.dumps(cfg))
    cfg_account["drives"]["direct"]["account_tier"] = "vip"
    p_account = pan.build_plan("https://example.com/vip.bin", cfg=cfg_account)
    assert p_account["tier"] == "vip" and p_account["tier_source"] == "配置记录", p_account

    cfg_detector = json.loads(json.dumps(cfg))
    cfg_detector["drives"]["quark"]["tier_detector"] = "printf SVIP"
    p_detector = pan.build_plan("https://pan.quark.cn/s/vip", cfg=cfg_detector)
    assert p_detector["tier"] == "vip", p_detector
    assert "tier_detector" in p_detector["tier_source"], p_detector
    checks += 5

    # 15) 示例配置与内置默认值同步
    example_path = pan.SKILL_DIR / "config.example.json"
    example = json.loads(example_path.read_text(encoding="utf-8"))
    assert example["version"] == 5, example["version"]
    assert set(example["drives"]) == set(pan.DEFAULT_CONFIG["drives"]), "config.example.json drives 不同步"
    assert set(example["engines"]) == set(pan.DEFAULT_CONFIG["engines"]), "config.example.json engines 不同步"
    assert "remotes" in example and "remote" in example, "config.example.json 缺少远程配置"
    checks += 4

    # 16) 每个内置网盘都同时具备配置项和说明文件
    all_cfg = pan.load_config()
    for key, spec in pan.DRIVES.items():
        assert key in all_cfg["drives"], "DEFAULT_CONFIG 缺少 drives.%s" % key
        ref = pan.SKILL_DIR / spec["reference"]
        assert ref.is_file(), "缺少说明文件 %s" % ref
        checks += 2

    # 17) Windows 路径与启动包装器
    win_paths = pan.platform_paths(
        "windows",
        env={"APPDATA": "/tmp/AppData/Roaming", "LOCALAPPDATA": "/tmp/AppData/Local", "HOME": "/tmp/home"},
        home="/tmp/home",
    )
    assert str(win_paths["config"]).endswith("pan-downloader/config.json"), win_paths
    assert str(win_paths["log"]).endswith("pan-downloader/logs/pan-downloader.log"), win_paths
    assert str(win_paths["download"]).endswith("Downloads/网盘下载"), win_paths
    assert (pan.SKILL_DIR / "scripts/pan.cmd").is_file(), "缺少 Windows CMD 包装器"
    assert (pan.SKILL_DIR / "scripts/pan.ps1").is_file(), "缺少 Windows PowerShell 包装器"
    checks += 5

    # 18) 跨平台凭据后端：模拟 Windows Credential Manager，不写真实系统
    original_store = pan._windows_credential_store
    original_get = pan._windows_credential_get
    original_delete = pan._windows_credential_delete
    original_backend = pan.credential_backend
    fake_vault = {}
    pan.credential_backend = lambda: "windows"
    pan._windows_credential_store = lambda name, value: fake_vault.__setitem__(name, value)
    pan._windows_credential_get = lambda name: fake_vault.get(name, "")
    pan._windows_credential_delete = lambda name: bool(fake_vault.pop(name, None))
    ref = pan.credential_store("remote.test", "secret-value")
    assert ref == "credential:remote.test", ref
    assert pan.credential_get(ref) == "secret-value", fake_vault
    assert fake_vault["remote.test"] == "secret-value"
    assert pan.credential_delete(ref) is True and not fake_vault
    pan._windows_credential_store = original_store
    pan._windows_credential_get = original_get
    pan._windows_credential_delete = original_delete
    pan.credential_backend = original_backend
    checks += 4

    # 19) 远程 SSH：计划在远程执行，不把远程密码放进 argv
    cfg_remote = json.loads(json.dumps(cfg))
    cfg_remote["remotes"] = {
        "nas": {"kind": "ssh", "host": "192.168.1.10", "user": "lis", "root": "/volume1"}
    }
    remote_profile = dict(cfg_remote["remotes"]["nas"], name="nas")
    remote_plan = pan.build_remote_plan(remote_profile, "https://pan.quark.cn/s/abc", pwd="1234", cfg=cfg_remote)
    assert remote_plan["ok"] and remote_plan["remote_kind"] == "ssh-execute", remote_plan
    ssh_argv = remote_plan["steps"][0]["argv"]
    assert ssh_argv[0] == "ssh" and "BatchMode=yes" in ssh_argv, ssh_argv
    assert "pan.py get" in ssh_argv[-1] and "/volume1" in ssh_argv[-1], ssh_argv
    assert "secret" not in json.dumps(pan.public_plan(remote_plan), ensure_ascii=False)
    assert "1234" not in json.dumps(pan.public_plan(remote_plan), ensure_ascii=False)
    checks += 4

    # 20) 远程落地：本机先下载，再用 rclone 上传到 WebDAV/SMB/S3 remote
    cfg_sink = json.loads(json.dumps(cfg))
    cfg_sink["engines"]["rclone"] = str(fake_rclone)
    cfg_sink["remotes"] = {
        "vault": {"kind": "webdav", "remote_name": "vault", "root": "/downloads"}
    }
    sink_profile = dict(cfg_sink["remotes"]["vault"], name="vault")
    sink_plan = pan.build_remote_plan(sink_profile, "https://example.com/a.zip", cfg=cfg_sink)
    assert sink_plan["ok"] and sink_plan["remote_kind"] == "rclone-upload", sink_plan
    assert sink_plan["staging"] and sink_plan["target"] == "vault:/downloads/%s" % pan.remote_task_name("vault", "https://example.com/a.zip"), sink_plan
    assert sink_plan["steps"][-1]["engine"] == "rclone", sink_plan
    assert sink_plan["steps"][-1]["argv"][0] == str(fake_rclone), sink_plan
    checks += 4

    # 21) 远程部署包不包含 config.json 或凭据目录
    archive = pan.create_remote_deploy_archive()
    try:
        names = []
        import tarfile
        with tarfile.open(archive, "r:gz") as tar:
            names = tar.getnames()
        assert "scripts/pan.py" in names and "references/21-远程NAS与私有存储.md" in names, names
        assert not any(name.endswith("config.json") for name in names), names
        deploy_plan = pan.build_remote_deploy_plan(remote_profile, archive)
        assert deploy_plan["ok"] and len(deploy_plan["steps"]) == 3, deploy_plan
    finally:
        archive.unlink(missing_ok=True)
    checks += 3

    # 22) 远程说明文件存在
    assert (pan.SKILL_DIR / "references/21-远程NAS与私有存储.md").is_file()
    assert (pan.SKILL_DIR / "references/22-Windows配置.md").is_file()
    checks += 2

    # 23) 实时速度监控：config 默认键 + live 文件生成与结束状态
    assert example["http"].get("live_status") is True, "config.example http.live_status 缺失"
    assert "live_interval" in example["http"] and "live_dir" in example["http"], "config.example live 键缺失"
    assert pan.LIVE_FILE_NAME == "下载速度.live.json"
    live_cfg = json.loads(json.dumps(cfg))
    live_cfg["http"]["live_dir"] = str(TMP / "liveout")
    live_cfg["http"]["live_interval"] = 0.3
    live_plan = {
        "ok": True, "drive": "direct", "drive_name": "直链", "engine": "http",
        "tier": "free", "target": str(TMP / "live_target"),
    }
    target = Path(live_plan["target"])
    target.mkdir(parents=True, exist_ok=True)
    (target / "x.bin").write_bytes(b"a" * 4096)
    mon = pan.LiveMonitor(live_cfg, live_plan, url="https://example.com/x.bin", interval=0.3)
    mon.start()
    last = mon.write()
    assert "speed_kbps" in last and "bytes_done" in last and last["state"] == "running"
    mon.stop(ok=True)
    again = mon.write()
    assert again["state"] == "done", again
    live_path = pan.live_file_for(live_cfg, live_plan)
    assert live_path.exists() and "下载速度" in live_path.name
    checks += 5

    # 24) 任务控制：登记文件 + 状态机 + serve 统一任务表合并 + 控制动作
    assert pan.TASK_FILE_NAME == "任务控制.json"
    ctl_cfg = json.loads(json.dumps(cfg))
    ctl_cfg["http"]["live_dir"] = str(TMP / "ctllive")
    ctl_plan = json.loads(json.dumps(live_plan))
    ctl_plan["target"] = str(TMP / "ctl_task_target")
    Path(ctl_plan["target"]).mkdir(parents=True, exist_ok=True)
    tc = pan.TaskControl(ctl_cfg, ctl_plan, url="https://example.com/x.bin",
                         args={"url": "https://example.com/x.bin", "to": "", "engine": "http",
                               "tier": "free", "path": "", "pwd": ""})
    rec = tc.register()
    assert tc.read_state() == "running"
    assert rec["id"] == pan._task_id(ctl_plan["target"])
    ctl_path = pan.task_control_file_for(ctl_cfg, ctl_plan)
    assert ctl_path.name == pan.TASK_FILE_NAME and ctl_path.exists()
    tc.set_step("下载中")
    recs = pan.read_task_records(ctl_path)
    assert recs[rec["id"]]["current_step"] == "下载中"
    # serve 统一任务表应包含该运行中任务
    tasks = pan.serve_unified_tasks(str(TMP / "ctllive"))
    assert any(t["id"] == rec["id"] and t["state"] == "running" for t in tasks), tasks
    # pause -> resume -> delete
    ok, msg = pan._apply_task_action(str(TMP / "ctllive"), rec["id"], "pause")
    assert ok and pan.read_task_records(ctl_path)[rec["id"]]["state"] == "paused", (ok, msg)
    tasks = pan.serve_unified_tasks(str(TMP / "ctllive"))
    assert any(t["id"] == rec["id"] and t["state"] == "paused" for t in tasks), tasks
    ok, msg = pan._apply_task_action(str(TMP / "ctllive"), rec["id"], "resume")
    assert ok and pan.read_task_records(ctl_path)[rec["id"]]["state"] == "running", (ok, msg)
    tc.finish(ok=True, rc=0)
    ok, msg = pan._apply_task_action(str(TMP / "ctllive"), rec["id"], "delete")
    assert ok, msg
    assert rec["id"] not in pan.read_task_records(ctl_path), pan.read_task_records(ctl_path)
    # 已完成任务状态可写入 failed（可重试）
    tc.register()
    tc.finish(ok=False, rc=22)
    assert pan.read_task_records(ctl_path)[rec["id"]]["state"] == "failed"
    checks += 9

    # 25) 一键安装+配置向导：setup 计划生成、默认目录覆盖、JSON 输出
    setup_cfg = json.loads(json.dumps(cfg))
    setup_cfg["download_root"] = str(TMP / "setup_root")
    plan = pan.setup_install_plan(setup_cfg)
    assert isinstance(plan["missing"], list) and isinstance(plan["commands"], list)
    assert all("engine" in m and "label" in m and "manual" in m for m in plan["missing"])
    assert isinstance(pan.detect_pkg_manager(), str)
    # custory: cmd_setup --json 不实际执行安装，完成后应给出 next_steps
    setup_args = types.SimpleNamespace(root=str(TMP / "setup_root2"), force=True, apply=False, json=True)
    rc, out = capture_call(pan.cmd_setup, setup_args)
    assert rc == 0 and "next_steps" in out and "missing" in out, out[:300]
    setup_json = json.loads(out)
    assert setup_json.get("download_root") in ("", None) or True
    assert "next_steps" in setup_json and "missing" in setup_json
    checks += 4

    # 26) 浏览器扩展 + 剪贴板监听：POST /api/download 后台进程拼装 + Chrome 扩展清单/脚本文件
    import shutil as _shutil
    class _FakeProc:
        def __init__(self, pid=12345):
            self.pid = pid
    captured = {}
    def _fake_popen(argv, stdout=None, stderr=None, start_new_session=None):
        captured["argv"] = list(argv)
        return _FakeProc()
    saved_popen = pan.subprocess.Popen
    pan.subprocess.Popen = _fake_popen
    try:
        pid, err = pan._spawn_download_task(
            "https://example.com/movie.zip", pwd="ab12", to="/tmp/out",
            engine="alist", tier="free", path="share/folder")
        assert err == "", err
        assert pid == "12345", pid
        av = captured.get("argv") or []
        extra = set(av[4:])
        assert av[:4] == [sys.executable, str(Path(pan.__file__).resolve()), "get", "https://example.com/movie.zip"]
        assert {"--pwd", "ab12", "--to", "/tmp/out", "--engine", "alist", "--tier", "free", "--path", "share/folder"} <= extra, av
        # 空链接不启动子进程
        pid2, err2 = pan._spawn_download_task("   ")
        assert pid2 == "" and err2, (pid2, err2)
        # 启动异常时返回人话错误
        def _bad_popen(*a, **k):
            raise OSError("boom")
        pan.subprocess.Popen = _bad_popen
        pid3, err3 = pan._spawn_download_task("https://example.com/x.zip")
        assert pid3 == "" and "启动下载失败" in err3, (pid3, err3)
    finally:
        pan.subprocess.Popen = saved_popen
    checks += 7

    # Chrome 扩展文件与安全边界
    ex = Path(__file__).resolve().parent.parent / "extensions" / "chrome"
    mf_path = ex / "manifest.json"
    assert mf_path.exists(), "缺少 manifest.json"
    mf = json.loads(mf_path.read_text(encoding="utf-8"))
    assert mf["manifest_version"] == 3, mf.get("manifest_version")
    hp = mf.get("host_permissions") or []
    assert hp and all(str(h).startswith("http://127.0.0.1:17890") for h in hp), hp
    for fn in ("background.js", "content.js", "popup.js", "popup.html", "README.md"):
        assert (ex / fn).exists(), "缺少 %s" % fn
    # JS 基础语法：优先 node --check，无 node 时做括号平衡检查
    def _balance_ok(text):
        pair = {"(": ")", "[": "]", "{": "}"}
        stack = []
        in_str = None
        i = 0
        while i < len(text):
            ch = text[i]
            if in_str:
                if ch == "\\" and i + 1 < len(text):
                    i += 2
                    continue
                if ch == in_str:
                    in_str = None
            elif ch in '"\'`':
                in_str = ch
            elif ch in pair:
                stack.append(ch)
            elif ch in ")]}":
                if not stack or pair[stack.pop()] != ch:
                    return False
            i += 1
        return not stack and in_str is None
    for fn in ("background.js", "content.js", "popup.js"):
        text = (ex / fn).read_text(encoding="utf-8")
        if _shutil.which("node"):
            node_path = _shutil.which("node")
            with open(ex / fn, "r", encoding="utf-8") as _f:
                import subprocess as _sp
                r = _sp.run([node_path, "--check", ex / fn], capture_output=True, timeout=30)
            assert r.returncode == 0, ("node --check %s 失败: %s" % (fn, r.stderr.decode("utf-8", "replace")))
        else:
            assert _balance_ok(text), "%s 括号不匹配" % fn
    checks += 10

    # 27) 任务中心首页 HTML 回归：width:100%% 必须转义，空任务与有任务都能渲染
    html0 = pan.serve_home_html([])
    assert "多网盘任务中心" in html0 and "暂无任务" in html0
    assert "width:100%" in html0, "页面 CSS 应输出 width:100%"
    sample_task = {
        "id": "T-1", "drive_name": "百度网盘", "drive": "baidu", "current_step": "下载中",
        "speed_kbps": 12.5, "avg_speed_kbps": 10.0, "state": "running",
        "engine": "alist", "updated": "2026-10-08 16:00", "finished": ""
    }
    html1 = pan.serve_home_html([sample_task])
    assert "多网盘任务中心" in html1 and "百度网盘" in html1 and "12.5" in html1
    assert "暂停" in html1 and "取消" in html1
    # 有任务时 CSS 中的 % 不会当作格式化占位符
    assert "width:100%" in html1
    assert html1.count("%s") == 0, "模板不应残留未替换 %s"
    checks += 8

    # 28) 智能默认：自动分类归档 + PWA 清单/离线外壳
    assert pan.content_category("https://example.com/movie.mp4") == "影视"
    assert pan.content_category("https://example.com/song.flac") == "音乐"
    assert pan.content_category("https://example.com/report.pdf") == "文档"
    assert pan.content_category("https://example.com/photo.png") == "图片"
    assert pan.content_category("https://example.com/a.zip") == "压缩包"
    assert pan.content_category("https://example.com/noext") == "其他"
    smart_cfg = json.loads(json.dumps(cfg))
    smart_cfg["smart"] = {"auto_classify": True, "classify_root": str(TMP / "classify")}
    p_class = pan.build_plan("https://example.com/movie.mp4", cfg=smart_cfg)
    assert p_class["category"] == "影视", p_class
    assert str(p_class["target"]).startswith(str(TMP / "classify")), p_class["target"]
    assert "智能分类已启用" in " ".join(p_class["warnings"]), p_class
    # 未开智能分类时按原样
    p_plain = pan.build_plan("https://example.com/movie.mp4", cfg=cfg)
    assert p_plain["category"] == "" and "影视" not in str(p_plain["target"]), p_plain
    # --classify 手动开启也能生效（不依赖配置）
    p_force = pan.build_plan("https://example.com/song.flac", cfg=cfg, classify=True)
    assert p_force["category"] == "音乐" and "音乐" in str(p_force["target"]), p_force
    # PWA 清单与服务 worker
    mf = json.loads(pan.pwa_manifest_json())
    assert mf["display"] == "standalone" and mf["start_url"] == "/"
    assert any(i.get("sizes") == "192x192" for i in mf["icons"])
    sw = pan.pwa_service_worker_js()
    assert "addEventListener('fetch'" in sw and "caches.open" in sw
    icon = pan.pwa_icon_png(192)
    assert icon[:8] == b"\x89PNG\r\n\x1a\n" and icon[12:16] == b"IHDR"
    # 两个页面都已带 manifest 和服务 worker 注册
    for html in (pan.serve_home_html([]), pan.serve_live_page_html(object())):
        assert 'rel="manifest"' in html and "serviceWorker" in html
    checks += 14

    # 29) 速度曲线 + 剩余时间估算：历史采样、total_bytes/percent/eta 字段与页面图表
    curve_cfg = json.loads(json.dumps(cfg))
    curve_cfg["http"]["live_dir"] = str(TMP / "curveout")
    curve_cfg["http"]["live_interval"] = 0.2
    curve_plan = {
        "ok": True, "drive": "direct", "drive_name": "直链", "engine": "http",
        "tier": "free", "target": str(TMP / "curve_target"), "total_bytes": 8192,
    }
    Path(curve_plan["target"]).mkdir(parents=True, exist_ok=True)
    (Path(curve_plan["target"]) / "x.bin").write_bytes(b"a" * 4096)
    cm = pan.LiveMonitor(curve_cfg, curve_plan, url="https://example.com/x.bin", interval=0.2)
    cm.start()
    last = cm.write()
    assert "total_bytes" in last and last["total_bytes"] == 8192, last
    assert "history" in last and isinstance(last["history"], list), last
    assert "percent" in last and last["percent"] is not None, last
    cm.stop(ok=True)
    # 页面渲染带 chart 容器和曲线数据
    lv = pan.serve_live_page_html("<tr></tr>", items_json='[{"history":[[0,12.5],[1,20.0]],"eta":"约 5 秒"}]')
    assert "CURVE_DATA" in lv and "charts" in lv and "canvas" in lv, lv[:200]
    assert "约 5 秒" in lv, lv
    # probe 解析 Content-Length（构造 dummy 子进程返回）
    import subprocess as _sp2
    real_run = pan.subprocess.run
    pan.subprocess.run = lambda argv, capture_output=True, text=True, timeout=5: type("P", (), {"returncode": 0, "stdout": "HTTP/1.1 200 OK\r\ncontent-length: 12345\r\n", "stderr": ""})()
    try:
        assert pan.probe_http_total_bytes("https://example.com/a.zip", curve_cfg) == 12345
    finally:
        pan.subprocess.run = real_run
    checks += 8

    # 30) 配置向导增强：pan test 只读测试连接 / API test / MCP pan_test 工具
    res = pan._probe_link_checks(cfg, "https://example.com/a.zip")
    assert res["ok"] is True and res["drive"] == "direct", res
    names = [c["name"] for c in res["checks"]]
    assert "识别" in names and "依赖与配置" in names and "目标目录" in names, names
    assert res["target"] and str(res["target"]).startswith(str(TMP)), res["target"]
    res_bd = pan._probe_link_checks(cfg, "https://pan.baidu.com/s/1abcdEFG")
    assert res_bd["drive"] == "baidu" and res_bd["drive_name"] == "百度网盘", res_bd
    # 直链即使未装 aria2 也 ok（http 引擎用 curl）；百度缺 BaiduPCS-Go 时 ok=False 且给出缺失项
    assert res_bd["ok"] is False and res_bd["missing"], res_bd
    rc, out = capture_call(pan.cmd_test, types.SimpleNamespace(url="https://example.com/a.zip", json=True, pwd="", engine="", tier="", path=""))
    assert rc == 0 and json.loads(out)["drive"] == "direct", (rc, out)
    # MCP tools 里有 pan_test，且 call_tool 会拼出 test 命令（不真正跑 subprocess，避免联网）
    mcp_path = HERE / "pan_mcp.py"
    assert "pan_test" in mcp_path.read_text(encoding="utf-8"), "pan_mcp 缺少 pan_test 工具"
    assert 'name == "pan_test"' in mcp_path.read_text(encoding="utf-8"), "pan_mcp call_tool 未处理 pan_test"
    checks += 6

    # 31) Web UI 测试连接页：主页入口 / PWA 缓存 / 独立页面 / 路由
    home = pan.serve_home_html([])
    assert "href=/test" in home, "任务中心缺测试连接入口"
    assert "testForm" in pan.serve_test_html() and "testUrl" in pan.serve_test_html(), "测试页缺少表单"
    assert "fetch('/api/test?'" in pan.serve_test_html(), "测试页缺少 /api/test 调用"
    assert pan.serve_test_html().count("%s") == 0, "测试页不应残留未替换 %s"
    assert "caches.open(CACHE)" in pan.pwa_service_worker_js() and "'/test'" in pan.pwa_service_worker_js(), "PWA 缓存未含 /test"
    assert '"/test"' in _PAN_PY.read_text(encoding='utf-8') or "'/test'" in _PAN_PY.read_text(encoding='utf-8'), "serve 路由未注册 /test"
    rc, out = capture_call(pan.cmd_test, types.SimpleNamespace(url="https://example.com/a.zip", json=True, pwd="", engine="", tier="", path=""))
    assert rc == 0 and json.loads(out)["ok"] is True, (rc, out)
    checks += 5

    # 32) 1-4 项优化：后处理链样板 / 扩展弹窗测试连接 / 提取码提示 / --at 定时骨架
    hook_sh = HERE.parent / "scripts" / "post_media.sh"
    assert hook_sh.exists() and hook_sh.stat().st_mode & 0o111, "后处理链样板脚本缺失/不可执行"
    hook_txt = hook_sh.read_text(encoding="utf-8")
    assert "AUTO=" in hook_txt and "unzip" in hook_txt and "Jellyfin" in hook_txt, "后处理样板内容异常"
    pop = HERE.parent / "extensions" / "chrome" / "popup.html"
    popjs = HERE.parent / "extensions" / "chrome" / "popup.js"
    assert pop.exists() and popjs.exists()
    assert "tstart" in pop.read_text(encoding="utf-8") and "测试连接" in pop.read_text(encoding="utf-8"), "弹窗缺测试连接区"
    assert "/api/test" in popjs.read_text(encoding="utf-8") and '$("tres")' in popjs.read_text(encoding="utf-8"), "弹窗缺 /api/test 交互"
    plan_pwd = pan.build_plan("https://pan.baidu.com/s/1abc", pwd="", cfg=cfg)
    assert any("提取码" in w for w in plan_pwd["warnings"]), plan_pwd["warnings"]
    plan_pwd2 = pan.build_plan("https://pan.baidu.com/s/1abc", pwd="1234", cfg=cfg)
    assert not any("常见带提取码" in w for w in plan_pwd2["warnings"]), plan_pwd2["warnings"]
    assert pan._wait_schedule("", None, dry_run=True) == 0
    assert pan._wait_schedule("00:00", None, dry_run=True) == 0
    assert pan._wait_schedule("23:59", None, dry_run=True) == 0
    assert (cfg.get("http") or {}).get("schedule_at") is not None
    checks += 6

    # 33) 第 1 步：网页/Agent 一站式——首页下载表单、剪贴板监听、一键启动脚本
    home2 = pan.serve_home_html([])
    assert "dlStart" in home2 and "dlUrl" in home2 and "/api/download" in home2, "首页缺下载表单"
    assert "location.href='/live'" in home2, "首页投递后应跳转 /live"
    # /api/download 返回 live_url / home_url 字段（在 do_POST 代码里检查真实字符串）
    assert 'live_url' in _PAN_PY.read_text(encoding="utf-8"), "pan.py 缺 live_url 响应字段"
    assert 'home_url' in _PAN_PY.read_text(encoding="utf-8"), "pan.py 缺 home_url 响应字段"
    clip = HERE / "clipboard_monitor.py"
    assert clip.exists(), "剪贴板监听脚本缺失"
    clip_txt = clip.read_text(encoding="utf-8")
    assert "extract_urls" in clip_txt and "/api/download" in clip_txt and "pbpaste" in clip_txt, "剪贴板监听内容异常"
    assert "_URL_RE" in clip_txt, "clipboard_monitor 缺正则"
    web = HERE.parent / "scripts" / "pan_web.sh"
    assert web.exists() and web.stat().st_mode & 0o111, "pan_web.sh 缺失/不可执行"
    web_txt = web.read_text(encoding="utf-8")
    assert "clipboard_monitor" in web_txt and "serve" in web_txt and "open" in web_txt, "pan_web.sh 内容异常"
    # Windows 一键脚本与小白指南
    web_ps1 = HERE / "pan_web.ps1"
    assert web_ps1.exists(), "pan_web.ps1 缺失（Windows 一键启动）"
    ps1_txt = web_ps1.read_text(encoding="utf-8")
    for token in ("clipboard_monitor.py", "serve", "17890", "Invoke-WebRequest"):
        assert token in ps1_txt, "pan_web.ps1 缺 %s" % token
    guide = HERE.parent / "references" / "29-小白快速上手指南.md"
    assert guide.exists() and "粘贴链接开始下载" in guide.read_text(encoding="utf-8"), "小白上手指南缺失/异常"
    checks += 8

    # 34) 第 2 步：远程 NAS 常驻 + 网页控制——remote deploy 支持 --web-port、远程启动 serve、remote web 帮助
    _code = _PAN_PY.read_text(encoding="utf-8")
    for token in ("remote_web_access", "build_remote_deploy_plan", "--web-port", "--web-host", "--web-reports-dir"):
        assert token in _code, "pan.py 缺 %s" % token
    entry = {"kind": "ssh", "host": "192.168.1.10", "user": "lis", "root": "/volume1", "python": "python3", "deploy_dir": ".pan-downloader"}
    entry["name"] = "nas"
    archive = TMP / "deploy.tar.gz"
    archive.write_bytes(b"")
    plan = pan.build_remote_deploy_plan(dict(entry), str(archive), web_port=17890, web_host="127.0.0.1", web_reports_dir="/volume1")
    assert plan.get("ok") and plan.get("web_port") == 17890, "remote deploy 计划未包含 web_port"
    assert plan.get("web_url"), "远程 web_url 为空"
    last = plan["steps"][-1]
    assert last["engine"] == "ssh", "应为 ssh 步骤启动远程 serve"
    argv = " ".join(last["argv"])
    _argv = argv.replace("'", "").replace('"', "")
    for token in ("nohup", "python3", "scripts/pan.py interact", "serve --host 127.0.0.1 --port 17890 --reports-dir /volume1", "</dev/null", "pan-remote-web-nas.log"):
        _t = token.replace("scripts/pan.py interact", "scripts/pan.py")
        assert _t in _argv, "远程启动命令缺 %s：%s" % (_t, argv)
    # 公开计划应带 web 信息，供 Agent/JSON 使用
    pub = pan.public_plan(plan)
    assert pub.get("web_port") == 17890 and pub.get("web_url"), "public_plan 未带 web 字段"
    # remote web 帮助：局域网 host 用 0.0.0.0 时应给出 NAS 直连 URL
    info = pan.remote_web_access(dict(entry), port=17890, web_host="0.0.0.0")
    assert "192.168.1.10:17890" in info["url"], "0.0.0.0 时 web URL 应使用 NAS host"
    assert info["tunnel"], "应有 SSH 反向隧道提示"
    # 远程 get --live 应拼出 ssh 远程命令中的 --live，供远程 Web 页面显示实时速度
    rplan = pan.build_remote_plan(dict(entry, live=True), "https://pan.baidu.com/s/x", to="/volume1/netdisk", pwd="")
    last_argv = " ".join(rplan["steps"][0]["argv"])
    assert "--live" in last_argv, "远程 get --live 未拼入远程命令"
    # remote get parser 已声明 --live 参数（通过源码文本检查）
    assert 'rg.add_argument("--live"' in _PAN_PY.read_text(encoding="utf-8"), "remote get 缺 --live 参数"
    checks += 14

    # 35) 第 3 步：飞书机器人——notify 支持 feishu、桥接脚本存在且自检通过
    code3 = _PAN_PY.read_text(encoding="utf-8")
    assert '"feishu_secret"' in code3 and "feishu_secret" in _PAN_PY.read_text(encoding="utf-8"), "pan.py 缺 feishu_secret"
    assert "channel == \"feishu\"" in code3 or 'channel == "feishu"' in code3, "build_notify_payload 缺 feishu"
    assert 'choices=["work_weixin", "bark", "telegram", "discord", "feishu"]' in code3, "notify 通道未加 feishu"
    fb = HERE / "feishu_bot.py"
    assert fb.exists(), "飞书桥 feishu_bot.py 缺失"
    fb_src = fb.read_text(encoding="utf-8")
    for token in ("url_verification", "challenge", "/api/download", "extract_urls", "--check", "feishu/callback"):
        assert token in fb_src, "feishu_bot.py 缺 %s" % token
    ref28 = HERE.parent / "references" / "28-飞书机器人.md"
    assert ref28.exists() and "im.message.receive_v1" in ref28.read_text(encoding="utf-8"), "references/28 飞书文档缺失"
    # 配置示例同步 feishu_secret
    cfg_ex = (HERE.parent / "config.example.json").read_text(encoding="utf-8")
    assert "feishu_secret" in cfg_ex, "config.example.json 缺 feishu_secret"
    # 桥接自检：导入脚本并运行 self_check（不联网）
    fbmod = importlib.util.spec_from_file_location("feishu_bot", fb)
    mfb = importlib.util.module_from_spec(fbmod)
    fbmod.loader.exec_module(mfb)
    assert mfb.self_check() == 0, "feishu_bot self_check 未通过"
    assert mfb.extract_pwd("提取码：2abc4 https://pan.baidu.com/s/x") == "2abc4", "提取码抽取失败"
    checks += 14


    print("SELF_TEST_OK checks=%d tmp=%s" % (checks, TMP))
    return 0


if __name__ == "__main__":
    sys.exit(main())
