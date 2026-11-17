# 分享：我写了个把幕布变成 Markdown 的小工具 mubu-integration

幕布的大纲很好用，但一直缺好用的命令行导出 / 备份，也没法让 AI Agent 直接读写。我逆向了幕布 Web 端用的一套接口，做了个非官方集成 mubu-integration：

- 一条命令把整本幕布导出成 Markdown（`export-tree`），标题 / `[x]` 勾选 / `> 备注` 往返保真；
- 反向 `create --md` 把 Markdown 导回幕布；
- 还能当 AI Agent 的 Skill，让 AI 直接读 / 写你的幕布。

诚实说：非官方逆向，读 / 导出零配置可用；但 `save` 写回受幕布 colla 成员 ID 限制（服务端不返回，需手动配 `MUBU_MEMBER_ID`）。CI 113 测试常绿。

```bash
npx skills add liuboacean/mubu-integration
python3 scripts/mubu_api.py export-tree --folder <id> --output ./backup
```

GitHub：https://github.com/liuboacean/mubu-integration

想问下大家：你们备份 / 导出幕布都用啥方案？有没有踩过接口变动的坑？欢迎交流。
