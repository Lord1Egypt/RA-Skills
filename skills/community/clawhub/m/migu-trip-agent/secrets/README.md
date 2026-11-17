# plan_multi_token.txt

将咪咕旅游 H5 登录后的 JWT 保存为本目录下的 **`plan_multi_token.txt`**（UTF-8，单行，无引号）。

## 获取方式

1. 打开 https://gulangyu.migudm.cn 并登录。
2. 开发者工具 → Network → 触发一次行程对话 → 从 WebSocket 的 `token=` 或 `Authorization` 复制 JWT（`eyJ` 开头，两个 `.`）。

## 预检

```bash
node ../scripts/plan_multi_ws_client.mjs --check-token --token-diagnostics
```

## 注意

- 勿将本文件提交到 git（已在 `.gitignore` 中忽略时以仓库配置为准）。
- 飞书粘贴可带 `Bearer ` 前缀，脚本会自动清洗。
