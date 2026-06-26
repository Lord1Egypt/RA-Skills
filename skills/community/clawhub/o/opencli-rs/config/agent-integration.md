# AI Agent 集成指南

本指南介绍如何将 OpenCLI 集成到 AI Agent 工作流中，让 AI 能够自动控制网站和桌面应用。

## 核心优势

1. **结构化输出** - JSON/YAML 格式，AI 可直接解析
2. **零 LLM 成本** - 无需消耗额外 token 解析非结构化数据
3. **确定性操作** - 相同命令始终返回相同结构
4. **广泛覆盖** - 50+ 平台和桌面应用

## 基础集成

### 1. 在 AGENT.md 中添加配置

```markdown
## OpenCLI 集成

使用 OpenCLI 自动化网站和桌面应用操作：

1. **发现可用命令**
   ```bash
   opencli list -f yaml
   ```

2. **执行操作**
   ```bash
   # 获取数据
   opencli bilibili hot --limit 10 -f json
   opencli zhihu hot -f json
   
   # 控制桌面应用
   opencli cursor send "分析代码"
   opencli antigravity ask "解释这个概念"
   ```

3. **处理结果**
   - 直接解析 JSON/YAML 输出
   - 转换为需要的数据结构
   - 保存到文件或数据库

4. **错误处理**
   ```bash
   # 诊断连接
   opencli doctor
   
   # 检查登录状态
   curl localhost:19825/status
   ```
```

### 2. 示例：AI Agent 工作流

```yaml
# AI Agent 工作流配置示例
workflows:
  collect_daily_data:
    steps:
      - name: 发现命令
        command: opencli list -f yaml | grep -E "(hot|trending|top)"
        
      - name: 收集数据
        commands:
          - opencli hackernews top --limit 20 -f json > hackernews.json
          - opencli github trending --limit 15 -f json > github.json
          - opencli bilibili hot --limit 10 -f json > bilibili.json
          
      - name: 分析数据
        command: |
          # AI 分析收集的数据
          cat *.json | your_analysis_script
          
      - name: 生成报告
        command: generate_report --inputs *.json --output report.md
```

## 进阶集成模式

### 模式1：数据收集 Agent

```bash
#!/bin/bash
# 数据收集 AI Agent

# 1. 动态发现可用数据源
DATA_SOURCES=$(opencli list -f yaml | yq '.[] | select(.category == "public" or .category == "browser") | .name')

# 2. 并发收集数据
for source in $DATA_SOURCES; do
    echo "收集 $source 数据..."
    opencli $source hot --limit 10 -f json > "data/${source}_$(date +%Y%m%d).json" &
done

# 3. 等待所有任务完成
wait

# 4. AI 处理和分析
# ... AI 处理逻辑 ...
```

### 模式2：桌面应用控制 Agent

```bash
#!/bin/bash
# 桌面应用控制 AI Agent

# 1. 检查应用状态
if opencli cursor status | grep -q "connected"; then
    echo "Cursor 已连接"
    
    # 2. 发送任务
    opencli cursor send "请分析以下代码并给出优化建议："
    opencli cursor send --file mycode.py
    
    # 3. 获取响应
    sleep 2
    response=$(opencli cursor read -f json)
    
    # 4. AI 处理响应
    echo "AI 分析 Cursor 响应..."
    # ... 处理逻辑 ...
fi
```

### 模式3：内容管理 Agent

```bash
#!/bin/bash
# 内容管理 AI Agent

# 1. 发现可下载内容
CONTENT_LIST=$(opencli xiaohongshu feed --limit 20 -f json)

# 2. AI 筛选感兴趣的内容
INTERESTING=$(echo "$CONTENT_LIST" | jq '.[] | select(.likes > 1000)')

# 3. 批量下载
echo "$INTERESTING" | jq -r '.id' | while read note_id; do
    opencli xiaohongshu download "$note_id" --output "./downloads/$note_id"
done

# 4. AI 分析下载的内容
# ... 分析逻辑 ...
```

## OpenClaw 特定集成

### 在 OpenClaw 技能中使用

```bash
# 在技能脚本中集成 OpenCLI
exec "npm install -g @jackwener/opencli"

# 配置 Chrome 扩展（需要手动步骤）
# 1. 下载扩展
# 2. 安装到 Chrome

# 在技能逻辑中使用
opencli list -f yaml > available_commands.yaml

# 根据用户请求执行相应命令
case $user_request in
    "获取B站热门")
        opencli bilibili hot --limit 10 -f table
        ;;
    "分析代码")
        opencli cursor send "$user_code"
        ;;
    "下载内容")
        opencli xiaohongshu download "$note_id"
        ;;
esac
```

### OpenClaw 技能模板

```markdown
# SKILL.md - OpenCLI 增强技能

## 使用时机
当用户需要：
- 自动化网站操作
- 收集多平台数据
- 控制桌面应用
- 下载和管理内容

## 工作流
1. 检查 OpenCLI 安装状态
2. 根据请求类型选择命令
3. 执行并解析结果
4. 格式化输出给用户

## 示例命令
```bash
# 在技能中调用
opencli ${platform} ${command} ${args} -f json
```

## 错误处理
```bash
# 技能中的错误处理
if ! opencli doctor; then
    echo "请安装 Chrome 扩展并登录目标网站"
fi
```
```

## 最佳实践

### 1. 命令发现与缓存
```bash
# 定期更新可用命令列表
opencli list -f yaml > ~/.opencli/available_commands.yaml

# AI Agent 读取缓存的命令
AVAILABLE_COMMANDS=$(cat ~/.opencli/available_commands.yaml)
```

### 2. 错误重试机制
```bash
# 带重试的命令执行
retry_command() {
    local cmd=$1
    local max_retries=3
    
    for i in $(seq 1 $max_retries); do
        if $cmd; then
            return 0
        fi
        echo "重试 $i/$max_retries..."
        sleep 2
    done
    return 1
}

# 使用示例
retry_command "opencli bilibili hot --limit 5 -f json"
```

### 3. 结果验证
```bash
# 验证命令结果
validate_result() {
    local result_file=$1
    local min_size=$2
    
    if [ ! -f "$result_file" ]; then
        echo "结果文件不存在"
        return 1
    fi
    
    local size=$(wc -c < "$result_file")
    if [ $size -lt $min_size ]; then
        echo "结果过小 ($size < $min_size)"
        return 1
    fi
    
    # 验证 JSON 格式
    if ! jq empty "$result_file" 2>/dev/null; then
        echo "无效的 JSON 格式"
        return 1
    fi
    
    return 0
}
```

### 4. 并发控制
```bash
# 控制并发数量
MAX_CONCURRENT=3
current_jobs=0

for task in "${tasks[@]}"; do
    # 等待空闲槽位
    while [ $current_jobs -ge $MAX_CONCURRENT ]; do
        sleep 1
        # 检查完成的任务
        current_jobs=$(jobs -r | wc -l)
    done
    
    # 启动任务
    opencli $task &
    ((current_jobs++))
done

# 等待所有任务完成
wait
```

## 监控与日志

### 1. 健康检查
```bash
# 定期健康检查
check_health() {
    # 检查 daemon 状态
    if ! curl -s localhost:19825/status | grep -q "ok"; then
        echo "Daemon 异常"
        return 1
    fi
    
    # 测试简单命令
    if ! opencli hackernews top --limit 1 -f json >/dev/null 2>&1; then
        echo "命令执行失败"
        return 1
    fi
    
    return 0
}

# 定时检查
while true; do
    if ! check_health; then
        # 触发恢复操作
        restart_daemon
    fi
    sleep 300  # 5分钟检查一次
done
```

### 2. 日志收集
```bash
# 收集执行日志
log_execution() {
    local command=$1
    local output_file=$2
    
    echo "[$(date)] 执行: $command" >> opencli.log
    $command > "$output_file" 2>> opencli_error.log
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "[$(date)] 成功: $command" >> opencli.log
    else
        echo "[$(date)] 失败($exit_code): $command" >> opencli.log
    fi
    
    return $exit_code
}
```

## 安全注意事项

### 1. 凭证管理
- OpenCLI 复用 Chrome 登录态，不存储明文凭证
- 确保只在受信任的环境中使用
- 定期检查 Chrome 登录状态

### 2. 权限控制
```bash
# 限制可执行的命令
ALLOWED_COMMANDS=("hackernews" "github" "arxiv" "wikipedia")
validate_command() {
    local cmd=$1
    
    for allowed in "${ALLOWED_COMMANDS[@]}"; do
        if [[ $cmd == $allowed* ]]; then
            return 0
        fi
    done
    
    echo "命令未授权: $cmd"
    return 1
}
```

### 3. 频率限制
```bash
# 实现简单的频率限制
last_execution=0
min_interval=10  # 最小间隔10秒

execute_with_rate_limit() {
    local current_time=$(date +%s)
    local time_since_last=$((current_time - last_execution))
    
    if [ $time_since_last -lt $min_interval ]; then
        local wait_time=$((min_interval - time_since_last))
        echo "等待 ${wait_time}秒..."
        sleep $wait_time
    fi
    
    "$@"
    last_execution=$(date +%s)
}
```

## 性能优化

### 1. 命令缓存
```bash
# 缓存常用命令结果
CACHE_DIR=~/.opencli/cache
CACHE_TTL=300  # 5分钟

get_cached_or_execute() {
    local cmd=$1
    local cache_key=$(echo "$cmd" | md5sum | cut -d' ' -f1)
    local cache_file="$CACHE_DIR/$cache_key"
    
    if [ -f "$cache_file" ]; then
        local cache_age=$(( $(date +%s) - $(stat -c %Y "$cache_file") ))
        if [ $cache_age -lt $CACHE_TTL ]; then
            cat "$cache_file"
            return
        fi
    fi
    
    # 执行并缓存
    $cmd | tee "$cache_file"
}
```

### 2. 批量操作
```bash
# 批量处理提高效率
batch_process() {
    local items=("$@")
    local batch_size=5
    
    for ((i=0; i<${#items[@]}; i+=batch_size)); do
        local batch=("${items[@]:i:batch_size}")
        
        # 并发处理批次
        for item in "${batch[@]}"; do
            process_item "$item" &
        done
        
        wait  # 等待批次完成
    done
}
```

## 扩展开发

### 1. 自定义适配器
参考 OpenCLI 文档创建自定义适配器：
- `CLI-EXPLORER.md` - 完整探索工作流
- `CLI-ONESHOT.md` - 快速命令生成

### 2. 插件开发
```bash
# 创建自定义插件
opencli plugin create my-plugin

# 开发工作流
1. 探索目标网站: opencli explore <url>
2. 生成适配器: opencli synthesize <site>
3. 测试命令: opencli <site> test
4. 发布插件: opencli plugin publish
```

---

通过以上集成指南，AI Agent 可以充分利用 OpenCLI 的能力，实现复杂的自动化和数据收集任务，同时保持高效和稳定。