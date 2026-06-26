# 01 - 項目結構

## 標準佈局

```
res://
├── project.godot           # 項目配置
├── export_presets.cfg      # 導出模板
│
├── scenes/                 # .tscn 文件（按類型組織）
│   ├── player/
│   │   ├── player.tscn
│   │   └── player_hud.tscn
│   ├── enemies/
│   │   ├── enemy_base.tscn
│   │   └── enemy_flying.tscn
│   ├── levels/
│   │   ├── level_01.tscn
│   │   └── level_02.tscn
│   └── ui/
│       ├── main_menu.tscn
│       ├── pause_menu.tscn
│       └── game_over.tscn
│
├── scripts/                # .gd 文件（鏡像 scenes/ 結構）
│   ├── player/
│   │   └── player.gd
│   ├── enemies/
│   │   ├── enemy_base.gd
│   │   └── enemy_flying.gd
│   ├── managers/
│   │   ├── game_manager.gd
│   │   └── audio_manager.gd
│   └── utils/
│       └── helpers.gd
│
├── assets/
│   ├── sprites/            # 2D 圖形
│   │   ├── characters/
│   │   └── environment/
│   ├── models/             # 3D 模型
│   ├── audio/
│   │   ├── sfx/
│   │   └── music/
│   ├── fonts/
│   └── shaders/
│
├── autoload/               # 單例腳本
│   ├── globals.gd
│   ├── events.gd
│   └── save_manager.gd
│
├── resources/              # .tres 文件
│   ├── themes/
│   └── data/
│
├── addons/                 # 插件
│   └── gdunit4/            # 測試框架
│
└── test/                   # GDUnit 測試
    ├── player/
    └── enemies/
```

## project.godot 配置

```ini
[application]
config/name="My Game"
config/version="1.0.0"
run/main_scene="res://scenes/ui/main_menu.tscn"
config/features=PackedStringArray("4.3", "GL Compatibility")
config/icon="res://assets/icon.svg"

[autoload]
Globals="*res://autoload/globals.gd"
Events="*res://autoload/events.gd"
SaveManager="*res://autoload/save_manager.gd"
AudioManager="*res://autoload/audio_manager.gd"

[display]
window/size/viewport_width=1920
window/size/viewport_height=1080
window/stretch/mode="canvas_items"
window/stretch/aspect="expand"

[input]
move_left={...}
move_right={...}
jump={...}
attack={...}

[rendering]
renderer/rendering_method="gl_compatibility"
textures/vram_compression/import_etc2_astc=true
```

## 命名規範

| 類型 | 規範 | 範例 |
|------|------|------|
| 場景 | snake_case.tscn | player_controller.tscn |
| 腳本 | snake_case.gd | player_controller.gd |
| 類名 | PascalCase | PlayerController |
| 函數 | snake_case | move_and_slide() |
| 變數 | snake_case | max_health |
| 常數 | SCREAMING_SNAKE | MAX_SPEED |

---

## ⚠️ AI PITFALL：路徑錯誤

```gdscript
# ❌ WRONG - 絕對路徑或相對路徑混用
var scene = load("/home/user/project/scenes/player.tscn")

# ✅ CORRECT - 使用 res:// 前綴
var scene = load("res://scenes/player.tscn")
```

## ⚠️ AI PITFALL：自動載入順序

```gdscript
# ❌ WRONG - 在 Globals 中存取 Events（如果 Events 在後面加載）
# globals.gd
func _ready():
    Events.something.connect(...)  # Events 可能還不存在

# ✅ CORRECT - 使用 call_deferred 或確保加載順序
func _ready():
    call_deferred("_connect_signals")

func _connect_signals():
    Events.something.connect(...)
```
