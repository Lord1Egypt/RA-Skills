# Kiro Hooks 配置参考

## 概述

Hooks 允许你自动化重复的开发任务，基于文件变化或开发事件触发。

## 配置文件

`.kiro/hooks.yaml`

## 触发器类型

### file.save
文件保存时触发

```yaml
hooks:
  - name: format-on-save
    trigger: file.save
    pattern: "*.ts"
    action: run "prettier --write {{file}}"
```

### file.create
文件创建时触发

```yaml
hooks:
  - name: add-header
    trigger: file.create
    pattern: "*.py"
    action: insert "{{file}}:1\n#!/usr/bin/env python3\n"
```

### file.delete
文件删除时触发

```yaml
hooks:
  - name: cleanup-test
    trigger: file.delete
    pattern: "src/**/*.ts"
    action: run "if [ -f {{test_file}} ]; then rm {{test_file}}; fi"
```

### git.commit
Git 提交时触发

```yaml
hooks:
  - name: run-tests-before-commit
    trigger: git.commit
    action: run "npm test"
```

### git.push
Git 推送时触发

```yaml
hooks:
  - name: deploy-on-push
    trigger: git.push
    branch: main
    action: run "vercel --prod"
```

### schedule
定时触发

```yaml
hooks:
  - name: daily-backup
    trigger: schedule
    cron: "0 2 * * *"  # 每天凌晨 2 点
    action: run "npm run backup"
```

## 动作类型

### run
执行 shell 命令

```yaml
action: run "npm run lint"
```

### insert
在文件指定位置插入内容

```yaml
action: insert "{{file}}:1\n// Created by Kiro\n"
```

### replace
替换文件内容

```yaml
action: replace
  pattern: "console\\.log\\(.*\\)"
  replacement: "// Removed console.log"
```

### notify
发送通知

```yaml
action: notify "Build completed!"
```

### chain
执行多个动作

```yaml
action: chain
  - run "npm run build"
  - run "npm test"
  - notify "CI passed!"
```

## 变量占位符

| 变量 | 描述 |
|------|------|
| `{{file}}` | 触发文件路径 |
| `{{filename}}` | 文件名（不含路径） |
| `{{dirname}}` | 文件所在目录 |
| `{{ext}}` | 文件扩展名 |
| `{{branch}}` | Git 分支名 |
| `{{timestamp}}` | 当前时间戳 |

## 条件执行

### 基于文件类型

```yaml
hooks:
  - name: frontend-lint
    trigger: file.save
    pattern: "src/**/*.{ts,tsx}"
    action: run "npm run lint:frontend"
    
  - name: backend-lint
    trigger: file.save
    pattern: "api/**/*.{py,go}"
    action: run "npm run lint:backend"
```

### 基于分支

```yaml
hooks:
  - name: prod-deploy
    trigger: git.push
    branch: main
    action: run "vercel --prod"
    
  - name: staging-deploy
    trigger: git.push
    branch: staging
    action: run "vercel"
```

### 基于环境变量

```yaml
hooks:
  - name: notify-team
    trigger: git.push
    branch: main
    if: env.CI_NOTIFY == "true"
    action: run "curl -X POST $SLACK_WEBHOOK"
```

## 错误处理

### 继续执行

```yaml
hooks:
  - name: optional-lint
    trigger: file.save
    action: run "npm run lint"
    onError: continue  # 失败也继续
```

### 停止执行

```yaml
hooks:
  - name: required-tests
    trigger: git.commit
    action: run "npm test"
    onError: abort  # 失败则中止
```

### 重试机制

```yaml
hooks:
  - name: flaky-api
    trigger: file.save
    action: run "npm run test:api"
    retry: 3  # 重试 3 次
    retryDelay: 1000  # 每次间隔 1 秒
```

## 最佳实践

### ✅ 推荐

- 快速操作（<5 秒）用于 save 触发器
- 使用 `onError: continue` 避免阻塞工作流
- 将耗时操作放在 git.push 或 schedule 触发器
- 使用 chain 组合相关操作

### ❌ 避免

- 网络请求用于 save 触发器（太慢）
- 无错误处理的强制操作
- 过于复杂的条件逻辑
- 修改工作目录外的文件

## 调试 Hooks

### 查看日志

```bash
kiro hooks logs --tail 50
```

### 测试 Hook

```bash
kiro hooks test <hook-name> --file <test-file>
```

### 禁用/启用

```bash
kiro hooks disable <hook-name>
kiro hooks enable <hook-name>
```

## 示例配置

### 完整项目配置

```yaml
hooks:
  # 代码质量
  - name: format-typescript
    trigger: file.save
    pattern: "**/*.ts"
    action: run "prettier --write {{file}}"
    onError: continue
    
  - name: lint-on-commit
    trigger: git.commit
    action: run "npm run lint"
    onError: abort
    
  # 测试
  - name: test-on-save
    trigger: file.save
    pattern: "**/*.test.ts"
    action: run "npm test -- {{file}}"
    
  - name: test-before-push
    trigger: git.push
    action: run "npm test"
    onError: abort
    
  # 部署
  - name: deploy-main
    trigger: git.push
    branch: main
    action: chain
      - run "npm run build"
      - run "vercel --prod"
      - notify "Production deployed!"
      
  # 备份
  - name: daily-backup
    trigger: schedule
    cron: "0 2 * * *"
    action: run "npm run backup"
```
