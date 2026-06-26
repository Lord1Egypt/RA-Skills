from pathlib import Path
import yaml


class CommandNotFound(Exception):
    pass


def load_menu_map(skill_root: Path) -> dict:
    p = skill_root / "references" / "menu_map.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return data


def resolve_command(skill_root: Path, command: str) -> dict:
    data = load_menu_map(skill_root)
    commands = data.get("commands", {})
    if command not in commands:
        raise CommandNotFound(f"未定义命令: {command}")
    return commands[command]
