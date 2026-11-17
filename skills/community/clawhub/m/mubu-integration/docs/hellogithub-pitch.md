# mubu-integration —— 把幕布变成可被命令行和 AI 操控的 Markdown 大纲

## 一句话
mubu-integration 是一个非官方但**真机验证可用**的幕布（Mubu）集成：用一条命令把幕布大纲导出为 Markdown、再导回去，还能让 AI Agent 直接读 / 写你的幕布知识库。

## 亮点
- **零配置读取 / 备份 / 导出**：只需手机号 + 密码，无需任何逆向技巧，`get` / `create` / `export-tree` / `list` / `search` 开箱即用。
- **Markdown 无损往返**：`create --md` 导入、`get --export markdown` 导出，`diff` 无差异（标题、`[x]` 勾选、`> 备注` 全部保真）。
- **可被 AI Agent 调用**：作为 Agent Skill，让 AI 把幕布当长期结构化记忆来读写。
- **整树导出 / OPML / FreeMind**：批量备份整个文件夹树，兼容 XMind 等大纲工具。
- **CI 113 测试 × 4 Python 版本常绿**，在非官方逆向项目里少见的健康度。

## 安装
```bash
npx skills add liuboacean/mubu-integration
pip install -r requirements.txt
```

## 3 条命令体验
```bash
export MUBU_PHONE=你的手机号
export MUBU_PASSWORD=你的密码
python3 scripts/mubu_api.py create "周会" --md examples/weekly.md   # Markdown → 幕布
python3 scripts/mubu_api.py get <doc-id> --export markdown > out.md  # 幕布 → Markdown
diff examples/weekly.md out.md                                      # 无输出 = 字节级一致
```

## 链接
- GitHub：https://github.com/liuboacean/mubu-integration
- 非官方集成，遵循幕布服务端限制；欢迎提 Issue / PR 同步新端点。
