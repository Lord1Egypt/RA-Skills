# Deploy

`link-transcriber` 的推荐部署方式是：

1. 部署你自己的上游转录/总结服务
2. 在服务端配置你自己的平台访问方式
3. 让公开 skill 指向你的 HTTPS API 地址

建议最少准备这些配置：

```env
LINK_TRANSCRIBER_UPSTREAM_ACCESS_XXHS=...
LINK_TRANSCRIBER_UPSTREAM_ACCESS_DOUYIN=...
LINK_TRANSCRIBER_MODEL=gemini-2.5-pro
```

如果你在 KnowledgeOS 工作区内维护该服务，可优先参考这些位置：

- `/Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/api`
- `/Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/web/doc/server-deployment-notes.md`

部署完成后，至少做这两步验证：

```bash
python3 scripts/check_service_health.py
python3 scripts/call_service_example.py 'https://xhslink.com/o/23s4jTem6em'
```

如果你使用公有托管服务，则最终用户不需要自己提供平台凭证。
