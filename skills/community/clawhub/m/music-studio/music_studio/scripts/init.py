"""init 命令：配置 Provider、模型、资源路径"""

import getpass
from pathlib import Path
from music_studio import config, providers


DEFAULT_OUTPUT = str(config.DEFAULT_OUTPUT_DIR.resolve())
DEFAULT_CONFIG = str(config.DEFAULT_CONFIG_DIR.resolve())


def _validate_api_key(api_key: str, provider: str) -> tuple[bool, str]:
    try:
        client = providers.get_api_client(api_key, provider)
        resp = client.lyrics_generation(prompt="test")
        client.raise_on_error(resp)
        return True, "ok"
    except Exception as e:
        return False, str(e)


def main(_=None):
    existing = config.load_config()

    if existing and config.is_configured():
        print(f"✅ 配置文件已存在: {config.CONFIG_FILE}")
        print(f"   输出目录: {config.get_output_dir()}")
        if existing.get("api_key"):
            print("   API Key 来源: config.json")
        else:
            print("   API Key 来源: 未设置")
        print("如需重新设置，请先运行: python -m music_studio reset")
        return

    print("=== Music Studio 初始化 ===\n")

    print("选择模型提供商：")
    print("  1) MiniMax (CN)")
    input("请选择 [1]: ").strip() or "1"
    provider = "minimax"

    print()
    print("请输入 API Key（将保存到 config.json）：")
    api_key = getpass.getpass("> ").strip()

    if not api_key:
        print("❌ API Key 不能为空")
        return

    print(f"\n🔑 正在校验 API Key...")
    ok, detail = _validate_api_key(api_key, provider)
    if ok:
        print("✅ API Key 验证通过")
    else:
        print(f"❌ API Key 验证失败：{detail}")
        return

    print()
    print("选择音乐模型（文本→音乐 / 翻唱最终生成）：")
    print("  1) music-2.6（推荐）")
    input("请选择 [1]: ").strip() or "1"
    music_model = "music-2.6"

    print()
    print("选择翻唱前处理模型：")
    print("  1) music-cover（仅用于前处理）")
    input("请选择 [1]: ").strip() or "1"
    cover_model = "music-cover"

    print()
    print("=== 资源路径配置 ===")
    print(f"当前默认输出目录：{DEFAULT_OUTPUT}")
    output_input = input("输出目录 [直接回车使用默认]: ").strip()
    output_dir = output_input if output_input else None

    print(f"\n当前默认配置目录：{DEFAULT_CONFIG}")
    print("(配置文件 config.json 所在位置，通常不需要改)")
    input("配置目录 [直接回车使用默认]: ").strip()

    data = {
        "provider": provider,
        "music_model": music_model,
        "cover_model": cover_model,
        "api_key": api_key,
    }
    if output_dir:
        data["output_dir"] = str(Path(output_dir).expanduser().resolve())

    config.save_config(data)

    print()
    print("✅ 配置已保存")
    print(f"   Provider: {provider}")
    print(f"   音乐/最终生成模型: {music_model}")
    print(f"   翻唱前处理模型: {cover_model}")
    print(f"   输出目录: {config.get_output_dir()}")
    print("   API Key: 已保存到 config.json")

    print()
    print("=== 开始使用 ===")
    print("📝 作词:     python -m music_studio lyrics \"<主题>\"")
    print("🎵 生成音乐: python -m music_studio music \"<描述>\"")
    print("🎙️ 翻唱:     python -m music_studio cover \"<描述>\" --audio <URL>")
    print("🔐 保存 Key: python -m music_studio set-key")
    print("🧹 清除 Key: python -m music_studio clear-key")
    print("📋 查看帮助: python -m music_studio help")
