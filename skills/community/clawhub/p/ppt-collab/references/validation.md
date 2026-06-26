# 验证方式

优先做和改动范围匹配的最小验证。

## 常用命令

### 整体启动

```bash
docker-compose up --build -d
```

适合需要联调前端、后端和 `export_tool` 的场景。

### 前端

工作目录：`frontend`

```bash
pnpm check
pnpm test
```

- `pnpm check` 适合 TS 类型和编译前静态检查
- `pnpm test` 适合已有 `vitest` 覆盖的 server 侧逻辑

### export_tool

工作目录：`export_tool`

```bash
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

适合排查 HTML -> PPTX 转换服务本身。

如果日志提示缺少 `dom-to-pptx.bundle.js`，到 `export_tool/dom-to-pptx` 执行：

```bash
pnpm install
pnpm build
```

### 后端导出 smoke test

工作目录：仓库根目录

```bash
python backend/test_new_pptx_export.py
```

这个脚本会生成一个测试 PPTX，适合在修改 HTML 转 PPTX 相关逻辑后快速验收。

## 验证建议

- 改 prompt 或 slide 布局：
  至少做一次生成结果的静态检查，确认没有突破 `1280x720` 画布假设。
- 改导出链路：
  除了跑服务，还应实际产出一个 `.pptx` 看文件是否生成成功。
- 改版本或编辑逻辑：
  至少检查创建版本、获取版本、更新单页这几条 API 的行为是否连贯。
- 改分享页 / 预览：
  注意浏览器预览正常不等于导出正常，必要时补一次导出验证。

## 当前已知情况

- 仓库里能直接看到的成熟自动化验证主要集中在前端 `vitest` 和导出 smoke test。
- 后端很多逻辑更偏集成链路，做修改时通常需要配合定向接口验证。
