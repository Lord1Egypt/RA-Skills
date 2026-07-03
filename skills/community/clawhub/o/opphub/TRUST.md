# 信任度与安全披露

## 当前可信度盘点（v1.0.3）

| 维度 | 状态 |
|------|------|
| 维护者 | ClawHub owner `mtty123456` |
| 源码 | https://github.com/mtty123456/opphub |
| 许可证 | MIT-0（任何人都可商用，无需署名） |
| ClawHub 自动扫描 | Skill Vetter + VirusTotal 通过 |

## 数据与隐私

- token 仅存在本地 `~/.opphub/agent.json`（权限 0600），不外发
- 不读本地 IM 通讯录 / 历史 / 文件
- 不假设使用者任何特定身份
- ClawHub 强制 MIT-0
- ClawHub 自动安全扫描基线通过

## 安全披露

发现问题，**不要开公开 issue**，请通过私下渠道提：

1. **GitHub Security Advisories**（推荐）
   - https://github.com/mtty123456/opphub/security/advisories/new
2. **维护者直连**
   - ClawHub owner `mtty123456` 私信

## 机器可验证

```bash
# 1. 看 ClawHub 元数据
clawhub skill inspect opphub

# 2. 看本地安装的 SKILL.md frontmatter
cat ~/.openclaw/skills/opphub/SKILL.md | head -20

# 3. 比对 homepage 与实际可达的 GitHub 链接
curl -I https://github.com/mtty123456/opphub

# 4. 看 token 本地保存是否合规
ls -la ~/.opphub/agent.json   # 应该 -rw-------
```
