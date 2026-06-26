"""reset 命令：一键重置，清除配置和输出，重新初始化"""

from music_studio import config, library as lib_mod


def main(_=None):
    print("=== Music Studio 重置 ===\n")

    # 读取当前输出目录（可能在自定义位置）
    current_output = config.get_output_dir()

    try:
        confirm = input("确定要重置吗？所有配置和输出记录将被清除 [y/N]: ").strip().lower()
    except (EOFError, AttributeError):
        confirm = ""

    if confirm not in ("y",):
        print("已取消")
        return

    # 清除配置
    if config.CONFIG_FILE.exists():
        config.CONFIG_FILE.unlink()
        print(f"✅ 已删除配置文件: {config.CONFIG_FILE}")

    # 清除输出记录
    lib_mod.purge_all()
    print(f"✅ 已清除输出目录: {current_output}")

    print("\n=== 开始重新初始化 ===\n")
    from music_studio.scripts import init
    init.main(_)