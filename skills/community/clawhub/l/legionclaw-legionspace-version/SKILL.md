---
name: legionspace-version
description: >
  检查大群空间 (LegionSpace, package: com.tongfudun.legion) 在各大应用商店的最新版本号。
  This skill should be used when the user asks to check LegionSpace versions, 大群空间版本,
  query app store versions for LegionSpace, or any request about the version status of
  the LegionSpace app across Chinese app stores.
  Covers: Apple App Store, Tencent MyApp, Xiaomi, vivo, Honor, Huawei, OPPO.
---

# LegionSpace 大群空间版本查询

查询 LegionSpace（包名 `com.tongfudun.legion`）在 7 大应用商店的最新版本号。

## 覆盖的应用商店

| # | 商店 | 查询方式 |
|---|------|----------|
| 1 | Apple App Store | iTunes Lookup API |
| 2 | Tencent MyApp (应用宝) | Playwright 渲染 |
| 3 | Xiaomi (小米) | Playwright 渲染 |
| 4 | vivo | Playwright 渲染 |
| 5 | Honor (荣耀) | Playwright 渲染 |
| 6 | Huawei AppGallery (华为) | Playwright 渲染 |
| 7 | OPPO | Playwright 渲染 |

## 执行方式

### Linux/macOS

```bash
bash ${SKILL_DIR}/scripts/大群空间版本查询.sh
```

### Windows

```bash
python ${SKILL_DIR}/scripts/legionspace_version_checker.py
```

入口脚本会自动完成以下步骤：
1. 检测 Python（`python3` / `python`）
2. 检查并安装依赖（`requests`、`playwright` + Chromium）
3. 依次查询 7 个应用商店
4. 结果输出到控制台，并保存到 `${SKILL_DIR}/scripts/LegionSpace_versions.txt`

也可直接调用 Python 脚本以跳过依赖检查：
```bash
python3 ${SKILL_DIR}/scripts/legionspace_version_checker.py
```

## 依赖

- Python 3.x
- `requests` — Apple API 查询
- `playwright` + Chromium — 渲染 JS 页面抓取版本号

## 代理说明

脚本已强制关闭代理（`no_proxy=*`，`trust_env=False`），确保直连各应用商店。

## 注意事项

- OPPO 应用商店仅限手机端访问，PC 端可能返回 `N/A`
- 部分商店（vivo、Honor、Huawei）页面加载较慢，超时设置已相应调整
- 整个过程约需 30-60 秒
- 报告文件：`${SKILL_DIR}/scripts/LegionSpace_versions.txt`
