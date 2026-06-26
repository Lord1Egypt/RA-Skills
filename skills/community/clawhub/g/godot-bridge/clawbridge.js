#!/usr/bin/env node
// ClawBridge - Godot Project Generator CLI v3.0

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PROJECT_DIR = process.cwd();

function generateProject(name, opts) {
  opts = opts || {};
  const projectDir = path.join(PROJECT_DIR, name);
  const is3D = opts.template === '3d' || opts['3d'];
  
  if (fs.existsSync(projectDir)) {
    console.error('Project "' + name + '" already exists');
    process.exit(1);
  }
  
  console.log('Creating Godot ' + (is3D ? '3D' : '2D') + ' project: ' + name);
  
  fs.mkdirSync(projectDir);
  fs.mkdirSync(path.join(projectDir, 'scenes'));
  fs.mkdirSync(path.join(projectDir, 'scripts'));
  fs.mkdirSync(path.join(projectDir, 'assets'));
  fs.mkdirSync(path.join(projectDir, 'levels'));
  fs.mkdirSync(path.join(projectDir, 'prefabs'));
  
  fs.writeFileSync(path.join(projectDir, 'project.godot'), '[application]\n\nconfig/name="' + name + '"\nrun/main_scene="res://scenes/main.tscn"\nconfig/features=PackedStringArray("4.2")\nconfig.icon="res://icon.svg"\n\n[autoload]\n\nGameManager="*res://scripts/game_manager.gd"\n\n[display]\n\nwindow/size/viewport_width=1280\nwindow/size/viewport_height=720\nwindow/stretch/mode="canvas_items"\n\n[rendering]\n\nrenderer/rendering_method="gl_compatibility"');
  
  fs.writeFileSync(path.join(projectDir, 'icon.svg'), '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128"><rect width="128" height="128" fill="#478cbf"/><polygon points="64,20 100,100 28,100" fill="#fff"/></svg>');
  
  fs.writeFileSync(path.join(projectDir, 'scenes', 'main.tscn'), '[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://scripts/main.gd" id="1_main"]\n\n[node name="Main" type="Node2D"]\nscript = ExtResource("1_main")\n\n[node name="Camera2D" type="Camera2D" parent="."]');
  
  fs.writeFileSync(path.join(projectDir, 'scripts', 'main.gd'), 'extends Node2D\n\nfunc _ready():\n\tprint("Game started!")\n');
  
  fs.writeFileSync(path.join(projectDir, 'scripts', 'game_manager.gd'), 'extends Node\n\nsignal game_started\nsignal player_stats_changed\n\nvar player_stats: Dictionary = {"hp": 100, "gold": 0, "level": 1}\nvar current_level: String = "main"\n\nfunc _ready():\n\tprint("GameManager ready")\n\nfunc add_gold(amount: int):\n\tplayer_stats["gold"] += amount\n\tplayer_stats_changed.emit()\n');
  
  console.log('Project created: ' + projectDir);
}

function generateScene(name, opts) {
  opts = opts || {};
  const scenesDir = path.join(PROJECT_DIR, 'scenes');
  if (!fs.existsSync(scenesDir)) {
    console.error('No project. Run "clawbridge init MyGame" first.');
    process.exit(1);
  }
  fs.writeFileSync(path.join(scenesDir, name + '.tscn'), '[gd_scene format=3]\n\n[node name="' + name + '" type="Node2D"]');
  console.log('Scene created: scenes/' + name + '.tscn');
}

function generateScript(name, opts) {
  opts = opts || {};
  const scriptsDir = path.join(PROJECT_DIR, 'scripts');
  if (!fs.existsSync(scriptsDir)) {
    console.error('No project. Run "clawbridge init MyGame" first.');
    process.exit(1);
  }
  const parentClass = opts.extends || 'Node';
  let content = 'extends ' + parentClass + '\n\n# ' + name + '.gd\n\n';
  content += 'func _ready():\n\tpass\n';
  fs.writeFileSync(path.join(scriptsDir, name + '.gd'), content);
  console.log('Script created: scripts/' + name + '.gd');
}

function generateLevel(name, opts) {
  const levelsDir = path.join(PROJECT_DIR, 'levels');
  if (!fs.existsSync(levelsDir)) {
    console.error('No project. Run "clawbridge init MyGame" first.');
    process.exit(1);
  }
  fs.writeFileSync(path.join(levelsDir, name + '.tscn'), '[gd_scene format=3]\n\n[node name="' + name + '" type="Node2D"]');
  console.log('Level created: levels/' + name + '.tscn');
}

function generateComponent(name, opts) {
  opts = opts || {};
  const scriptsDir = path.join(PROJECT_DIR, 'scripts');
  if (!fs.existsSync(scriptsDir)) {
    console.error('No project. Run "clawbridge init MyGame" first.');
    process.exit(1);
  }
  
  let content = 'extends Node\n\n# ' + name + '.gd - Game Component\n\n';
  
  switch (opts.type) {
    case 'health':
      content += 'var max_health: float = 100\nvar current_health: float = max_health\n\nsignal health_changed\nsignal died\n\nfunc take_damage(amount: float):\n\tcurrent_health -= amount\n\thealth_changed.emit()\n\tif current_health <= 0:\n\t\tdied.emit()\n\nfunc heal(amount: float):\n\tcurrent_health = min(max_health, current_health + amount)\n\thealth_changed.emit()\n';
      break;
    case 'inventory':
      content += 'var items: Array = []\nvar gold: int = 0\nvar max_slots: int = 20\n\nsignal inventory_changed\n\nfunc add_item(item_name: String) -> bool:\n\tif items.size() >= max_slots: return false\n\titems.append({"name": item_name})\n\tinventory_changed.emit()\n\treturn true\n\nfunc remove_item(item_name: String):\n\tfor i in range(items.size()):\n\t\tif items[i].name == item_name:\n\t\t\titems.remove_at(i)\n\t\t\tinventory_changed.emit()\n\t\t\treturn\n';
      break;
    case 'save':
      content += 'var save_path: String = "user://save.dat"\n\nfunc save_game():\n\tvar data = {"player": GameManager.player_stats, "level": GameManager.current_level}\n\tvar file = FileAccess.open(save_path, FileAccess.WRITE)\n\tfile.store_string(JSON.stringify(data))\n\tfile.close()\n\tprint("Saved!")\n\nfunc load_game():\n\tif not FileAccess.file_exists(save_path): return false\n\tvar file = FileAccess.open(save_path, FileAccess.READ)\n\tGameManager.player_stats = JSON.parse_string(file.get_as_text())\n\tfile.close()\n\tprint("Loaded!")\n\treturn true\n';
      break;
    case 'input':
      content += 'func get_direction() -> float:\n\treturn Input.get_axis("left", "right")\n\nfunc is_jump_pressed() -> bool:\n\treturn Input.is_action_just_pressed("jump")\n';
      break;
    case 'dialogue':
      content += 'var current_lines: Array = []\nvar current_index: int = 0\n\nsignal line_displayed(text: String)\nsignal dialogue_ended\n\nfunc show(lines: Array):\n\tcurrent_lines = lines\n\tcurrent_index = 0\n\tnext()\n\nfunc next():\n\tif current_index < current_lines.size():\n\t\tline_displayed.emit(current_lines[current_index])\n\t\tcurrent_index += 1\n\telse:\n\t\tdialogue_ended.emit()\n';
      break;
    case 'quest':
      content += 'var active_quests: Array = []\nvar completed_quests: Array = []\n\nsignal quest_started(name: String)\nsignal quest_completed(name: String)\n\nfunc start_quest(quest_name: String, target: int):\n\tactive_quests.append({"name": quest_name, "progress": 0, "target": target})\n\tquest_started.emit(quest_name)\n\nfunc update_quest(quest_name: String, progress: int):\n\tfor q in active_quests:\n\t\tif q.name == quest_name:\n\t\t\tq.progress = progress\n\t\t\tif q.progress >= q.target:\n\t\t\t\tcomplete_quest(quest_name)\n\nfunc complete_quest(quest_name: String):\n\tfor q in active_quests:\n\t\tif q.name == quest_name:\n\t\t\tactive_quests.erase(q)\n\t\t\tcompleted_quests.append(q)\n\t\t\tquest_completed.emit(quest_name)\n';
      break;
    default:
      content += 'func _ready():\n\tprint("Component: ' + name + '")\n';
  }
  
  fs.writeFileSync(path.join(scriptsDir, name + '.gd'), content);
  console.log('Component created: scripts/' + name + '.gd');
}

function generateAsset(name, opts) {
  opts = opts || {};
  const assetsDir = path.join(PROJECT_DIR, 'assets');
  if (!fs.existsSync(assetsDir)) {
    console.error('No project. Run "clawbridge init MyGame" first.');
    process.exit(1);
  }
  
  const posArgs = opts._ || [];
  
  // Determine asset type from command or first positional arg
  let assetType = opts.type || 'image';
  let fileName = name;
  
  // Handle: asset image player.png or asset sound jump.wav
  if (name === 'image' || name === 'sound' || name === 'audio') {
    assetType = name;
    fileName = posArgs[0] || 'asset';
  }
  
  switch (assetType) {
    case 'image':
    case 'img':
      const width = opts.width || 64;
      const height = opts.height || 64;
      const color = opts.color || '#478cbf';
      const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + width + '" height="' + height + '"><rect width="' + width + '" height="' + height + '" fill="' + color + '"/></svg>';
      const imgName = fileName.replace(/\.(png|svg|jpg)$/, '') + '.svg';
      fs.writeFileSync(path.join(assetsDir, imgName), svg);
      console.log('Image placeholder created: assets/' + imgName);
      break;
      
    case 'sound':
    case 'audio':
      const audioContent = '# Audio placeholder\n# Replace with actual audio file\n# Supported formats: .wav, .ogg, .mp3\n';
      const ext = fileName.endsWith('.wav') ? '.wav' : fileName.endsWith('.ogg') ? '.ogg' : fileName.endsWith('.mp3') ? '.mp3' : '.wav';
      const audioFileName = fileName.replace(/\.(wav|ogg|mp3)$/, '') + ext;
      fs.writeFileSync(path.join(assetsDir, audioFileName), audioContent);
      console.log('Audio placeholder created: assets/' + audioFileName + ' (replace with actual file)');
      break;
      
    default:
      console.log('Unknown asset type: ' + assetType);
  }
}

function generateMaterial(name, opts) {
  opts = opts || {};
  const resourcesDir = path.join(PROJECT_DIR, 'resources');
  if (!fs.existsSync(resourcesDir)) {
    fs.mkdirSync(resourcesDir);
  }
  
  const materialType = opts.type || 'standard';
  const color = opts.color || '1, 1, 1, 1';
  
  let content = '[gd_resource type="StandardMaterial3D" format=3]\n\n';
  content += '[resource]\n';
  content += 'albedo_color = Color(' + color + ')\n';
  
  if (opts.metallic) {
    content += 'metallic = ' + opts.metallic + '\n';
  }
  if (opts.roughness) {
    content += 'roughness = ' + opts.roughness + '\n';
  }
  
  fs.writeFileSync(path.join(resourcesDir, name + '.tres'), content);
  console.log('Material created: resources/' + name + '.tres');
}

function generateAnimation(name, opts) {
  opts = opts || {};
  const resourcesDir = path.join(PROJECT_DIR, 'resources');
  if (!fs.existsSync(resourcesDir)) {
    fs.mkdirSync(resourcesDir);
  }
  
  const tracks = opts.tracks || 1;
  const duration = opts.duration || 1.0;
  
  let content = '[gd_resource type="Animation" format=3]\n\n';
  content += '[resource]\n';
  content += 'resource_name = "' + name + '"\n';
  content += 'length = ' + duration + '\n';
  content += 'loop_mode = ' + (opts.loop ? '1' : '0') + '\n';
  content += 'step = 0.1\n\n';
  
  // Add track for position
  content += 'tracks/0/type = "value"\n';
  content += 'tracks/0/imported = false\n';
  content += 'tracks/0/enabled = true\n';
  content += 'tracks/0/path = NodePath(".:position")\n';
  content += 'tracks/0/interp = 1\n';
  content += 'tracks/0/loop_wrap = true\n';
  content += 'tracks/0/keys = {\n';
  content += '"times": PackedFloat32Array(0, ' + duration + '),\n';
  content += '"transitions": PackedFloat32Array(1, 1),\n';
  content += '"update": 0,\n';
  content += '"values": [Vector2(0, 0), Vector2(0, 0)]\n';
  content += '}\n';
  
  fs.writeFileSync(path.join(resourcesDir, name + '.anim'), content);
  console.log('Animation created: resources/' + name + '.anim');
}

function generateUI(name, opts) {
  opts = opts || {};
  const scenesDir = path.join(PROJECT_DIR, 'scenes');
  const scriptsDir = path.join(PROJECT_DIR, 'scripts');
  
  if (!fs.existsSync(scenesDir)) {
    console.error('No project. Run "clawbridge init MyGame" first.');
    process.exit(1);
  }
  
  const uiType = opts.type || name;
  const sceneName = name;
  
  switch (uiType) {
    case 'menu':
    case 'main_menu':
      // Generate main menu scene
      const menuScene = '[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://scripts/menu.gd" id="1"]\n\n[node name="Menu" type="Control"]\nlayout_mode = 3\nanchors_preset = 15\nanchor_right = 1.0\nanchor_bottom = 1.0\ngrow_horizontal = 2\ngrow_vertical = 2\nscript = ExtResource("1")\n\n[node name="Background" type="ColorRect" parent="."]\nlayout_mode = 1\nanchors_preset = 15\nanchor_right = 1.0\nanchor_bottom = 1.0\ngrow_horizontal = 2\ngrow_vertical = 2\ncolor = Color(0.1, 0.1, 0.15, 1)\n\n[node name="VBoxContainer" type="VBoxContainer" parent="."]\nlayout_mode = 1\nanchors_preset = 8\nanchor_left = 0.5\nanchor_top = 0.5\nanchor_right = 0.5\nanchor_bottom = 0.5\noffset_left = -120\noffset_top = -100\noffset_right = 120\noffset_bottom = 100\ngrow_horizontal = 2\ngrow_vertical = 2\n\n[node name="Title" type="Label" parent="VBoxContainer"]\nlayout_mode = 2\ntext = "GAME TITLE"\nhorizontal_alignment = 1\nvertical_alignment = 1\n\n[node name="PlayButton" type="Button" parent="VBoxContainer"]\nlayout_mode = 2\ntext = "Play"\n\n[node name="OptionsButton" type="Button" parent="VBoxContainer"]\nlayout_mode = 2\ntext = "Options"\n\n[node name="QuitButton" type="Button" parent="VBoxContainer"]\nlayout_mode = 2\ntext = "Quit"\n';
      fs.writeFileSync(path.join(scenesDir, 'menu.tscn'), menuScene);
      
      // Generate menu script
      const menuScript = 'extends Control\n\nfunc _ready():\n\t$VBoxContainer/PlayButton.pressed.connect(_on_play_pressed)\n\t$VBoxContainer/OptionsButton.pressed.connect(_on_options_pressed)\n\t$VBoxContainer/QuitButton.pressed.connect(_on_quit_pressed)\n\nfunc _on_play_pressed():\n\tget_tree().change_scene_to_file("res://scenes/main.tscn")\n\nfunc _on_options_pressed():\n\tprint("Options menu")\n\nfunc _on_quit_pressed():\n\tget_tree().quit()\n';
      fs.writeFileSync(path.join(scriptsDir, 'menu.gd'), menuScript);
      console.log('UI created: scenes/menu.tscn + scripts/menu.gd');
      break;
      
    case 'hud':
    case 'score':
      // Generate HUD scene
      const hudScene = '[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://scripts/hud.gd" id="1"]\n\n[node name="HUD" type="CanvasLayer"]\nscript = ExtResource("1")\n\n[node name="TopBar" type="HBoxContainer" parent="."]\nanchors_preset = 10\nanchor_right = 1.0\noffset_left = 10\noffset_top = 10\noffset_right = -10\noffset_bottom = 60\ngrow_horizontal = 2\n\n[node name="HPContainer" type="VBoxContainer" parent="TopBar"]\nlayout_mode = 2\n\n[node name="HPLabel" type="Label" parent="TopBar/HPContainer"]\nlayout_mode = 2\ntext = "HP"\n\n[node name="HPBar" type="ProgressBar" parent="TopBar/HPContainer"]\ncustom_minimum_size = Vector2(150, 20)\nlayout_mode = 2\nmax_value = 100.0\nvalue = 100.0\n\n[node name="ScoreContainer" type="VBoxContainer" parent="TopBar"]\nlayout_mode = 2\nsize_flags_horizontal = 3\n\n[node name="ScoreLabel" type="Label" parent="TopBar/ScoreContainer"]\nlayout_mode = 2\ntext = "Score: 0"\nhorizontal_alignment = 2\n\n[node name="GoldContainer" type="VBoxContainer" parent="TopBar"]\nlayout_mode = 2\n\n[node name="GoldLabel" type="Label" parent="TopBar/GoldContainer"]\nlayout_mode = 2\ntext = "Gold: 0"\n';
      fs.writeFileSync(path.join(scenesDir, 'hud.tscn'), hudScene);
      
      // Generate HUD script
      const hudScript = 'extends CanvasLayer\n\n@onready var hp_bar = $TopBar/HPContainer/HPBar/HPBar\n@onready var score_label = $TopBar/ScoreContainer/ScoreLabel\n@onready var gold_label = $TopBar/GoldContainer/GoldLabel\n\nfunc _ready():\n\tGameManager.player_stats_changed.connect(update_stats)\n\tupdate_stats()\n\nfunc update_stats():\n\tvar stats = GameManager.player_stats\n\tif hp_bar:\n\t\thp_bar.max_value = stats.get("max_hp", 100)\n\t\thp_bar.value = stats.get("hp", 100)\n\tif score_label:\n\t\tscore_label.text = "Score: " + str(stats.get("score", 0))\n\tif gold_label:\n\t\tgold_label.text = "Gold: " + str(stats.get("gold", 0))\n';
      fs.writeFileSync(path.join(scriptsDir, 'hud.gd'), hudScript);
      console.log('UI created: scenes/hud.tscn + scripts/hud.gd');
      break;
      
    case 'dialog':
    case 'dialogue':
      // Generate dialogue scene
      const dialogScene = '[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://scripts/dialogue_ui.gd" id="1"]\n\n[node name="DialogueUI" type="CanvasLayer"]\nscript = ExtResource("1")\n\n[node name="Panel" type="PanelContainer" parent="."]\nvisible = false\nanchors_preset = 7\nanchor_left = 0.5\nanchor_top = 1.0\nanchor_right = 0.5\nanchor_bottom = 1.0\noffset_left = -200\noffset_top = -150\noffset_right = 200\noffset_bottom = -20\ngrow_horizontal = 2\n\n[node name="VBoxContainer" type="VBoxContainer" parent="Panel"]\nlayout_mode = 2\n\n[node name="SpeakerLabel" type="Label" parent="Panel/VBoxContainer"]\nlayout_mode = 2\ntext = "Speaker"\n\n[node name="TextLabel" type="Label" parent="Panel/VBoxContainer"]\nlayout_mode = 2\ntext = "Dialogue text..."\nautowrap_mode = 2\n\n[node name="NextButton" type="Button" parent="Panel/VBoxContainer"]\nlayout_mode = 2\ntext = "Next >>"\n';
      fs.writeFileSync(path.join(scenesDir, 'dialogue.tscn'), dialogScene);
      
      // Generate dialogue script
      const dialogScript = 'extends CanvasLayer\n\nvar dialogue_lines: Array = []\nvar current_line: int = 0\nvar speaker_name: String = ""\n\nsignal dialogue_started\nsignal dialogue_ended\n\nfunc _ready():\n\t$Panel.visible = false\n\t$Panel/VBoxContainer/NextButton.pressed.connect(_on_next_pressed)\n\nfunc start(speaker: String, lines: Array):\n\tspeaker_name = speaker\n\tdialogue_lines = lines\n\tcurrent_line = 0\n\t$Panel.visible = true\n\tdialogue_started.emit()\n\tshow_line()\n\nfunc show_line():\n\tif current_line < dialogue_lines.size():\n\t\t$Panel/VBoxContainer/SpeakerLabel.text = speaker_name\n\t\t$Panel/VBoxContainer/TextLabel.text = dialogue_lines[current_line]\n\telse:\n\t\tend()\n\nfunc _on_next_pressed():\n\tcurrent_line += 1\n\tshow_line()\n\nfunc end():\n\t$Panel.visible = false\n\tdialogue_ended.emit()\n';
      fs.writeFileSync(path.join(scriptsDir, 'dialogue_ui.gd'), dialogScript);
      console.log('UI created: scenes/dialogue.tscn + scripts/dialogue_ui.gd');
      break;
      
    case 'inventory':
      // Generate inventory scene
      const invScene = '[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://scripts/inventory_ui.gd" id="1"]\n\n[node name="InventoryUI" type="CanvasLayer"]\nscript = ExtResource("1")\n\n[node name="Panel" type="PanelContainer" parent="."]\nvisible = false\nanchors_preset = 7\nanchor_left = 0.5\nanchor_top = 0.5\nanchor_right = 0.5\nanchor_bottom = 0.5\noffset_left = -200\noffset_top = -150\noffset_right = 200\noffset_bottom = 150\ngrow_horizontal = 2\ngrow_vertical = 2\n\n[node name="VBoxContainer" type="VBoxContainer" parent="Panel"]\nlayout_mode = 2\n\n[node name="Title" type="Label" parent="Panel/VBoxContainer"]\nlayout_mode = 2\ntext = "INVENTORY"\nhorizontal_alignment = 1\n\n[node name="GridContainer" type="GridContainer" parent="Panel/VBoxContainer"]\nlayout_mode = 2\ncolumns = 5\n\n[node name="GoldLabel" type="Label" parent="Panel/VBoxContainer"]\nlayout_mode = 2\ntext = "Gold: 0"\n\n[node name="CloseButton" type="Button" parent="Panel/VBoxContainer"]\nlayout_mode = 2\ntext = "Close"\n';
      fs.writeFileSync(path.join(scenesDir, 'inventory.tscn'), invScene);
      
      // Generate inventory script
      const invScript = 'extends CanvasLayer\n\nvar inventory_size: int = 20\nvar items: Array = []\nvar gold: int = 0\n\nfunc _ready():\n\t$Panel.visible = false\n\t$Panel/VBoxContainer/CloseButton.pressed.connect(close)\n\t# Initialize inventory slots\n\tfor i in range(inventory_size):\n\t\tvar slot = Label.new()\n\t\tslot.text = "[Empty]"\n\t\t$Panel/VBoxContainer/GridContainer.add_child(slot)\n\nfunc open():\n\t$Panel.visible = true\n\tupdate_display()\n\nfunc close():\n\t$Panel.visible = false\n\nfunc update_display():\n\tvar slots = $Panel/VBoxContainer/GridContainer.get_children()\n\tfor i in range(slots.size()):\n\t\tif i < items.size():\n\t\t\tslots[i].text = items[i].get("name", "Item")\n\t\telse:\n\t\t\tslots[i].text = "[Empty]"\n\t$Panel/VBoxContainer/GoldLabel.text = "Gold: " + str(gold)\n\nfunc add_item(item_name: String) -> bool:\n\tif items.size() >= inventory_size:\n\t\treturn false\n\titems.append({"name": item_name, "count": 1})\n\tupdate_display()\n\treturn true\n\nfunc remove_item(item_name: String) -> bool:\n\tfor i in range(items.size()):\n\t\tif items[i].name == item_name:\n\t\t\titems.remove_at(i)\n\t\t\tupdate_display()\n\t\t\treturn true\n\treturn false\n';
      fs.writeFileSync(path.join(scriptsDir, 'inventory_ui.gd'), invScript);
      console.log('UI created: scenes/inventory.tscn + scripts/inventory_ui.gd');
      break;
      
    default:
      console.log('Unknown UI type: ' + uiType);
  }
}

// ========== Level Editor ==========
const LEVEL_DATA_FILE = '.clawbridge_level.json';

function getLevelData() {
  try {
    if (fs.existsSync(LEVEL_DATA_FILE)) {
      return JSON.parse(fs.readFileSync(LEVEL_DATA_FILE, 'utf8'));
    }
  } catch (e) {}
  return { name: 'main', objects: [] };
}

function saveLevelData(data) {
  fs.writeFileSync(LEVEL_DATA_FILE, JSON.stringify(data, null, 2));
}

let currentLevelData = getLevelData();

function handleLevelCommand(subCmd, extraArgs, opts) {
  const levelsDir = path.join(PROJECT_DIR, 'levels');
  if (!fs.existsSync(levelsDir)) {
    console.error('No project. Run "clawbridge init MyGame" first.');
    process.exit(1);
  }
  const addOpts = parseArgs(extraArgs);
  const levelName = addOpts._[0] || currentLevelData.name;
  
  switch (subCmd) {
    case 'create':
    case 'new':
      currentLevelData.name = levelName;
      currentLevelData.objects = [];
      saveLevelData(currentLevelData);
      console.log('Level created: ' + levelName + ' (use "level add" to add objects)');
      break;
    case 'add':
      const objType = extraArgs[0] || 'object';
      const objX = addOpts.x || 100;
      const objY = addOpts.y || 100;
      const objName = addOpts._[1] || objType;
      currentLevelData.objects.push({ type: objType, name: objName, x: objX, y: objY });
      saveLevelData(currentLevelData);
      console.log('Added ' + objType + ' at (' + objX + ', ' + objY + ')');
      break;
    case 'save':
      saveLevel(levelsDir);
      break;
    case 'load':
      loadLevel(levelsDir, extraArgs[0] || currentLevelData.name);
      saveLevelData(currentLevelData);
      break;
    case 'list':
      const files = fs.readdirSync(levelsDir);
      console.log('Levels: ' + files.filter(f => f.endsWith('.tscn')).map(f => f.replace('.tscn', '')).join(', '));
      break;
    case 'clear':
      currentLevelData.objects = [];
      saveLevelData(currentLevelData);
      console.log('Level cleared');
      break;
    case 'show':
      console.log('Level: ' + currentLevelData.name + ', Objects: ' + currentLevelData.objects.length);
      for (const obj of currentLevelData.objects) {
        console.log('  - ' + obj.type + ' "' + obj.name + '" at (' + obj.x + ', ' + obj.y + ')');
      }
      break;
    default:
      console.log('level create <name>   Create level');
      console.log('level add <type> --x 100 --y 200   Add object');
      console.log('level save           Save level');
      console.log('level load <name>    Load level');
      console.log('level list           List levels');
      console.log('level show           Show objects');
  }
}

function saveLevel(levelsDir) {
  const ln = currentLevelData.name;
  let content = '[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://scripts/level.gd" id="1"]\n\n[node name="' + ln + '" type="Node2D"]\nscript = ExtResource("1")\nlevel_name = "' + ln + '"\n\n[node name="Camera2D" type="Camera2D" parent="."]\ncurrent = true\n\n';
  for (const obj of currentLevelData.objects) {
    content += '[node name="' + obj.name + '" type="' + (obj.type === 'enemy' || obj.type === 'player' ? 'CharacterBody2D' : obj.type === 'coin' || obj.type === 'item' ? 'Area2D' : 'Node2D') + '" parent="."]\nposition = Vector2(' + obj.x + ', ' + obj.y + ')\n\n';
  }
  fs.writeFileSync(path.join(levelsDir, ln + '.tscn'), content);
  fs.writeFileSync(path.join(levelsDir, ln + '.json'), JSON.stringify(currentLevelData, null, 2));
  console.log('Level saved: levels/' + ln + '.tscn');
}

function loadLevel(levelsDir, levelName) {
  const jp = path.join(levelsDir, levelName + '.json');
  if (!fs.existsSync(jp)) { console.error('Level not found: ' + levelName); return; }
  currentLevelData = JSON.parse(fs.readFileSync(jp, 'utf8'));
  console.log('Level loaded: ' + levelName + ' (' + currentLevelData.objects.length + ' objects)');
}

function generateObject(type, opts) {
  opts = opts || {};
  const scenesDir = path.join(PROJECT_DIR, 'scenes');
  if (!fs.existsSync(scenesDir)) {
    console.error('No project. Run "clawbridge init MyGame" first.');
    process.exit(1);
  }
  
  // Determine if 3D project
  const projectGodot = path.join(PROJECT_DIR, 'project.godot');
  const is3D = fs.existsSync(projectGodot) && fs.readFileSync(projectGodot, 'utf8').includes('Node3D');
  
  const mainScenePath = path.join(scenesDir, is3D ? 'main_3d.tscn' : 'main.tscn');
  if (!fs.existsSync(mainScenePath)) {
    console.error('No main scene. Run "clawbridge init" first.');
    process.exit(1);
  }
  
  let content = fs.readFileSync(mainScenePath, 'utf8');
  const posArgs = opts._ || [];
  const nodeName = posArgs[0] || type;
  
  // 2D objects
  if (!is3D) {
    const x = opts.x || 100;
    const y = opts.y || 100;
    let nodeType = 'Node2D';
    let extraContent = '';
    
    switch (type) {
      case 'rigid':
      case 'physics':
        nodeType = 'RigidBody2D';
        const mass2d = opts.mass || 1.0;
        extraContent = '\n[node name="CollisionShape2D" type="CollisionShape2D" parent="."]\nshape = RectangleShape2D.new()\n';
        break;
      case 'area':
        nodeType = 'Area2D';
        extraContent = '\n[node name="CollisionShape2D" type="CollisionShape2D" parent="."]\nshape = RectangleShape2D.new()\n';
        break;
      case 'static':
        nodeType = 'StaticBody2D';
        extraContent = '\n[node name="CollisionShape2D" type="CollisionShape2D" parent="."]\nshape = RectangleShape2D.new()\n';
        break;
      case 'joint':
        nodeType = 'PinJoint2D';
        break;
      case 'label':
        nodeType = 'Label';
        break;
      case 'button':
        nodeType = 'Button';
        break;
      case 'box':
      case 'sphere':
        nodeType = 'MeshInstance2D';
        break;
      case 'camera':
        nodeType = 'Camera2D';
        break;
      case 'light':
        nodeType = 'Node2D';
        break;
      case 'particles':
        nodeType = 'CPUParticles2D';
        break;
      case 'character':
        nodeType = 'CharacterBody2D';
        extraContent = '\n[node name="CollisionShape2D" type="CollisionShape2D" parent="."]\nshape = CapsuleShape2D.new()\n';
        break;
      default:
        nodeType = 'Node2D';
    }
    
    content += '\n[node name="' + nodeName + '" type="' + nodeType + '" parent="."]\nposition = Vector2(' + x + ', ' + y + ')\n';
    content += extraContent;
  } else {
    // 3D objects
    const x = opts.x || 0;
    const y = opts.y || 0;
    const z = opts.z || 0;
    
    let nodeType = 'Node3D';
    let extraProps = '';
    
    switch (type) {
      case 'cube':
        nodeType = 'MeshInstance3D';
        extraProps = 'mesh = BoxMesh.new()\n';
        break;
      case 'sphere':
        nodeType = 'MeshInstance3D';
        extraProps = 'mesh = SphereMesh.new()\n';
        break;
      case 'mesh':
        nodeType = 'MeshInstance3D';
        const meshFile = posArgs[0] || 'model.obj';
        extraProps = '# Load mesh: ' + meshFile + '\n';
        break;
      case 'terrain':
        nodeType = 'MeshInstance3D';
        const size = opts.size || 100;
        extraProps = 'mesh = PlaneMesh.new()\nmesh.size = Vector2(' + size + ', ' + size + ')\n';
        break;
      case 'camera':
      case 'camera3d':
        nodeType = 'Camera3D';
        extraProps = 'current = true\n';
        break;
      case 'light':
      case 'light3d':
        nodeType = 'DirectionalLight3D';
        extraProps = 'shadow_enabled = true\n';
        break;
      case 'character':
      case 'character3d':
        nodeType = 'CharacterBody3D';
        break;
      case 'physics':
        // physics rigid --mass 1.0
        // physics kinematic --speed 200
        // physics area --detect player
        const physType = posArgs[0] || 'rigid';
        const mass = opts.mass || 1.0;
        const speed = opts.speed || 200;
        
        if (physType === 'rigid') {
          nodeType = 'RigidBody3D';
          extraProps = 'mass = ' + mass + '\n';
          // Add collision shape
          extraProps += '\n[node name="CollisionShape3D" type="CollisionShape3D" parent="."]\nshape = BoxShape3D.new()\n';
        } else if (physType === 'kinematic') {
          nodeType = 'CharacterBody3D';
          extraProps = '# kinematic body, speed = ' + speed + '\n';
        } else if (physType === 'area') {
          nodeType = 'Area3D';
          const detect = opts.detect || 'player';
          extraProps = '# area detection: ' + detect + '\n';
        } else if (physType === 'joint' || physType === 'spring') {
          nodeType = 'Generic6DOFJoint3D';
          extraProps = '# spring joint\nangular_limit_x/z = 1.0\n';
        }
        break;
      default:
        if (type === 'box' || type === 'sphere') {
          nodeType = 'MeshInstance3D';
          extraProps = 'mesh = ' + (type === 'box' ? 'BoxMesh.new()' : 'SphereMesh.new()') + '\n';
        }
    }
    
    content += '\n[node name="' + nodeName + '" type="' + nodeType + '" parent="."]\n';
    content += 'transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, ' + x + ', ' + y + ', ' + z + ')\n';
    content += extraProps;
  }
  
  fs.writeFileSync(mainScenePath, content);
  console.log('Created ' + type + ': ' + nodeName + (is3D ? ' (3D)' : ''));
}

function parseArgs(args) {
  const options = {};
  let posArgs = [];
  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    if (!arg.startsWith('-')) { posArgs.push(arg); i++; continue; }
    const key = arg.replace(/^-+/, '');
    const nextArg = args[i + 1];
    const hasValue = nextArg && !nextArg.startsWith('-');
    if (hasValue) { options[key] = isNaN(nextArg) ? nextArg : parseFloat(nextArg); i += 2; }
    else { options[key] = true; i++; }
  }
  options._ = posArgs;
  return options;
}

// ========== Export ==========
function exportProject(platform, opts) {
  opts = opts || {};
  const projectFile = path.join(PROJECT_DIR, 'project.godot');
  if (!fs.existsSync(projectFile)) {
    console.error('No project. Run "clawbridge init MyGame" first.');
    process.exit(1);
  }
  
  const exportDir = path.join(PROJECT_DIR, 'export');
  if (!fs.existsSync(exportDir)) {
    fs.mkdirSync(exportDir);
  }
  
  // Map platform names to Godot export presets
  const platformMap = {
    'html5': 'Web',
    'web': 'Web',
    'windows': 'Windows',
    'win': 'Windows',
    'macos': 'macOS',
    'mac': 'macOS',
    'linux': 'Linux',
    'android': 'Android',
    'ios': 'iOS',
    'iphone': 'iOS'
  };
  
  const godotPlatform = platformMap[platform.toLowerCase()] || platform;
  
  console.log('Exporting for ' + godotPlatform + '...');
  console.log('');
  console.log('To export, you need:');
  console.log('1. Godot 4.x installed');
  console.log('2. Export templates installed');
  console.log('');
  console.log('Run manually:');
  console.log('  godot --headless --export-release "' + godotPlatform + '" "./export/"');
  console.log('');
  console.log('Or use Godot Editor:');
  console.log('  Project > Export > ' + godotPlatform);
  
  // Create export_presets.cfg
  createExportPresets(godotPlatform);
  
  console.log('');
  console.log('Created: export_presets.cfg');
}

function createExportPresets(platform) {
  const presets = '[preset.0]\n\nname="' + platform + '"\nplatform="' + platform + '"\nrunnable=true\ncustom_features=""\nexport_filter="all_resources"\nexclude_filter=""\ninclude_filter=""\nexport_path="export/' + platform.toLowerCase() + '/index.html"\npatch_list=PackedStringArray()\nscript_export_mode=1\nscript_encryption_key=""\n';
  
  fs.writeFileSync(path.join(PROJECT_DIR, 'export_presets.cfg'), presets);
}

function printUsage() {
  console.log('ClawBridge v3.0 - Godot Project Generator\n');
  console.log('Usage: clawbridge <command> [options]\n');
  console.log('=== Project ===');
  console.log('  init <name>                   Create project');
  console.log('  init <name> --template rpg     RPG template');
  console.log('  init <name> --3d               3D project');
  console.log('\n=== Generate ===');
  console.log('  scene <name>           Generate scene');
  console.log('  script <name>          Generate script');
  console.log('  level <name>          Generate level');
  console.log('\n=== Components ===');
  console.log('  component <name> --type health      Health system');
  console.log('  component <name> --type inventory   Inventory');
  console.log('  component <name> --type save        Save/Load');
  console.log('  component <name> --type input       Input');
  console.log('  component <name> --type dialogue   Dialogue');
  console.log('  component <name> --type quest       Quest');
  console.log('\n=== Resources ===');
  console.log('  asset image <name>            Create image placeholder');
  console.log('  asset sound <name>             Create audio placeholder');
  console.log('  material <name>                 Create material');
  console.log('  animation <name>                Create animation');
  console.log('\n=== Level Editor ===');
  console.log('  level create <name>    Create new level');
  console.log('  level add <type> --x 100 --y 200   Add object');
  console.log('  level save            Save level');
  console.log('  level load <name>     Load level');
  console.log('  level list            List levels');
  console.log('  level show            Show objects');
  console.log('  level clear           Clear objects');
  console.log('\n=== UI Generator ===');
  console.log('  ui menu                       Main menu');
  console.log('  ui hud                        HUD display');
  console.log('  ui dialog                     Dialogue box');
  console.log('  ui inventory                  Inventory UI');
  console.log('\n=== Objects ===');
  console.log('  label "Text" --x 100 --y 50');
  console.log('  button "Click" --x 200');
  console.log('  box --x 100 --y 100');
  console.log('  camera --x 640 --y 360');
  console.log('\n=== Physics (2D) ===');
  console.log('  physics rigid --mass 1.0       Rigid body');
  console.log('  physics kinematic --speed 200  Kinematic body');
  console.log('  physics area --detect player   Area detection');
  console.log('  physics joint                Joint/constraint');
  console.log('\n=== Physics (3D) ===');
  console.log('  physics rigid --mass 1.0       3D Rigid body');
  console.log('  physics kinematic             3D Kinematic body');
  console.log('  physics area                  3D Area');
  console.log('  physics joint                 3D Joint/Spring');
  console.log('\n=== Export ===');
  console.log('  export html5              Export HTML5/Web');
  console.log('  export windows            Export Windows');
  console.log('  export macos              Export macOS');
  console.log('  export linux              Export Linux');
  console.log('  export android            Export Android');
  console.log('  export ios                Export iOS');
  console.log('\n=== Run ===');
  console.log('  open    Open in Godot');
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) { printUsage(); return; }
  const cmd = args[0];
  const opts = parseArgs(args.slice(1));
  
  switch (cmd) {
    case 'init':
    case 'new':
      generateProject(args[1] || 'MyGame', opts);
      break;
    case 'scene':
      generateScene(args[1] || 'Scene', opts);
      break;
    case 'script':
      generateScript(args[1] || 'Script', opts);
      break;
    case 'level':
      handleLevelCommand(args[1] || 'show', args.slice(2), opts);
      break;
    case 'component':
    case 'comp':
      generateComponent(args[1] || 'Component', opts);
      break;
    case 'asset':
      generateAsset(args[1] || 'asset', opts);
      break;
    case 'material':
      generateMaterial(args[1] || 'Material', opts);
      break;
    case 'animation':
      generateAnimation(args[1] || 'Animation', opts);
      break;
    case 'ui':
      generateUI(args[1] || 'ui', opts);
      break;
    case 'level':
      handleLevelCommand(args[1] || 'level', args.slice(2), opts);
      break;
    case 'label':
    case 'button':
    case 'box':
    case 'sphere':
    case 'camera':
    case 'light':
    case 'particles':
    case 'character':
    case 'cube':
    case 'mesh':
    case 'terrain':
    case 'physics':
      generateObject(cmd, opts);
      break;
    case 'open':
      try { execSync('godot --path "' + PROJECT_DIR + '"', { stdio: 'inherit' }); }
      catch (e) { console.log('Install Godot: https://godotengine.org'); }
      break;
    case 'export':
      exportProject(args[1] || 'html5', opts);
      break;
    default:
      console.log('Unknown command: ' + cmd);
      printUsage();
      process.exit(1);
  }
}

main();
