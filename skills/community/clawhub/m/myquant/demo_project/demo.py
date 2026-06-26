def main():
    print("🤖 MyQuant (掘金量化) 实际框架导入演示")
    try:
        from gm.api import set_token, history_n
        print("✅ 掘金量化 API 导入成功。")
        print("使用前需配置: set_token('YOUR_TOKEN')")
    except ImportError:
        print("❌ 未安装 gm 包 (pip install gm)")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    main()
