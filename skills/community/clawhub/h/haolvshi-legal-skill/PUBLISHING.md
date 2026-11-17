# 技能包托管与下载说明

这里的“托管”是指把安装文档、技能压缩包和技能图标放到官网，供用户或人工智能工具下载安装；它与法律咨询、计算器、合同审核等应用的在线地址无关。服务器托管只是完整发布的一部分，完整发布还必须同步 GitHub 和 ClawHub；Claude 不发布。

打包命令、版本递增、rsync 路径和官网构建步骤见 `README.md` 的「打包与发布」。每次生成 zip 前必须递增版本号；线上仍覆盖不带版本号的固定下载地址。

## 托管文件

将安装文件放到官网的以下目录：

```text
/skills/haolvshi-legal-skill/INSTALL.md
/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip
/skills/haolvshi-legal-skill/haolvshi-legal-skill-icon.png
```

对应下载地址：

- `https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/INSTALL.md`
- `https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip`
- `https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill-icon.png`

## 静态路由要求

官网的 `/skills/` 应作为静态文件路径处理。找不到文件时返回 404，不能回退到官网首页。

参考配置：

```nginx
location ^~ /skills/ {
    alias /站点静态目录/skills/;
    try_files $uri =404;
    default_type application/octet-stream;
}
```

建议让 `INSTALL.md` 返回 `text/markdown; charset=utf-8`，技能压缩包返回 `application/zip` 或 `application/octet-stream`。

## 下载验证

上传后逐一验证：

```bash
curl -I https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/INSTALL.md
curl -I https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip
curl -I https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill-icon.png
```

检查响应能够直接返回相应文件，并确认下载文件校验值与 `dist/checksums.txt` 一致。

命令行安装可以使用官网压缩包地址。正式发布仍需按仓库根目录 `AGENTS.md` 和 `发布平台说明.md` 同步 GitHub 公开仓库与 Release、ClawHub。Claude 不发布；WorkBuddy 两类专用包只在本地生成和校验，不自动打开页面或上传。

命令行安装命令：

```bash
npx skills add https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip --skill haolvshi-legal-skill
```
