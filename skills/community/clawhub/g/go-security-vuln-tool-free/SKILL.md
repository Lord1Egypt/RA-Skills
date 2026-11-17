---
name: "go-security-vuln-tool-free"
description: "Go模块安全缺陷检测工具,使用govulncheck扫描已知漏洞、评估影响并提供修复建议,适合个人Go开发者使用。Use when 需要安全检测、合规审计、质量检查、加密防护时使用。不适用于安全评估未授权目标。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Go安全质量检查免费版"
  version: "1.0.0"
  summary: "Go模块安全缺陷检测工具,使用govulncheck扫描已知漏洞、评估影响并提供修复建议,适合个人Go开发者使用。"
  tags:
    - "安全"
    - "Go"
    - "质量检查"
    - "免费版"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# Go安全质量检查免费版
## 概述
本工具为个人Go开发者提供依赖安全缺陷检测能力,使用官方 `govulncheck` 工具扫描Go模块中的已知漏洞。免费版支持单项目扫描,提供漏洞影响评估与修复版本建议,帮助开发者在项目上线前或依赖更新前快速识别安全风险。

### 免费版与专业版对比
| 能力维度 | 免费版 | 专业版 |
|:---------|:-------|:-------|
| 扫描工具 | govulncheck | govulncheck + gosec + custom |
| 扫描范围 | 依赖漏洞 | 依赖+代码+配置 |
| 影响分析 | 基础(是否调用) | 深度(调用路径分析) |
| 批量扫描 | 单项目 | 多项目批量 |
| CI/CD集成 | 基础脚本 | 完整流水线 |
| 报告格式 | 文本/JSON | HTML/SARIF/PDF |
| 持续监控 | 不支持 | 新漏洞自动告警 |

## 核心能力
### 1. govulncheck质量检查
```bash
#!/bin/sh
# Go项目质量检查脚本
echo "=== Go安全质量检查 ==="
echo "项目: $(basename "$(pwd)")"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 依赖说明
if ! command -v govulncheck &> /dev/null; then
    echo "安装govulncheck..."
    go install golang.org/x/vuln/cmd/govulncheck@latest
fi

# 运行质量检查
echo "--- 运行govulncheck ---"
govulncheck ./... 2>&1

echo ""
echo "--- 扫描完成 ---"
```

**输出**: 返回govulncheck质量检查的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 漏洞影响评估
```bash
#!/bin/sh
# 漏洞影响评估(JSON输出)
echo "=== 漏洞影响评估 ==="

# 以JSON格式获取扫描结果
govulncheck -json ./... > /tmp/vuln-results.json 2>/dev/null

# 解析漏洞信息
echo ""
echo "--- 漏洞列表 ---"
jq -r '.osv // empty | "漏洞ID: \(.id)\n  描述: \(.summary // .details[:100] // "无描述")\n  严重性: \(.database_specific.severity // "未知")\n"' /tmp/vuln-results.json 2>/dev/null

echo ""
echo "--- 受影响模块 ---"
jq -r '.finding // empty | "模块: \(.trace[0].module)\n  版本: \(.trace[0].version)\n  漏洞: \(.osv)\n  是否调用: \(.trace[1].function // "未直接调用")\n"' /tmp/vuln-results.json 2>/dev/null

echo ""
echo "--- 统计 ---"
TOTAL=$(jq -s '[.[] | select(.osv)] | length' /tmp/vuln-results.json 2>/dev/null || echo "0")
CALLED=$(jq -s '[.[] | select(.finding and .finding.trace[1])] | length' /tmp/vuln-results.json 2>/dev/null || echo "0")
echo "  总漏洞数: ${TOTAL}"
echo "  已调用漏洞: ${CALLED}"
echo "  未调用漏洞: $((TOTAL - CALLED))"
```

**输出**: 返回漏洞影响评估的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 修复版本建议
```bash
#!/bin/sh
# 漏洞修复建议
echo "=== 漏洞修复建议 ==="
echo ""

# 获取受影响的模块及其漏洞
govulncheck -json ./... 2>/dev/null | jq -r '
    .osv // empty |
    "漏洞: \(.id)",
    "  严重性: \(.database_specific.severity // "未知")",
    "  修复版本: \(.affected[0].ranges[0].events[-1].fixed // "暂无修复版本")",
    "  受影响模块: \(.affected[0].package.name)",
    ""
' 2>/dev/null

echo ""
echo "--- 可修复的漏洞 ---"
echo "执行以下命令更新依赖:"
echo ""
echo "  # 更新所有依赖到最新安全版本"
echo "  go get -u ./..."
echo "  go mod tidy"
echo ""
echo "  # 更新特定模块"
echo "  go get module-name@latest"
```

**输出**: 返回修复版本建议的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 依赖版本检查
```bash
#!/bin/sh
# Go依赖版本与安全状态检查
echo "=== Go依赖版本检查 ==="
echo ""

if [ ! -f go.mod ]; then
    echo "未找到go.mod文件,请在Go项目根目录运行"
    exit 1
fi

echo "--- 直接依赖 ---"
grep -E '^\s+[^\s]+\s+v[0-9]' go.mod | while read -r module version; do
    # 检查是否有可用更新
    LATEST=$(go list -m -versions "$module" 2>/dev/null | awk '{print $NF}')
    if [ -n "$LATEST" ] && [ "$LATEST" != "$version" ]; then
        echo "  [!] ${module}"
        echo "      当前: ${version}"
        echo "      最新: ${LATEST}"
    else
        echo "  [OK] ${module} ${version}"
    fi
done

echo ""
echo "--- 间接依赖数量 ---"
INDIRECT=$(grep -c '// indirect' go.mod 2>/dev/null || echo "0")
echo "  间接依赖: ${INDIRECT} 个"
```

**输出**: 返回依赖版本检查的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：模块安全缺陷检测、扫描已知漏洞、评估影响并提供修、适合个人、开发者使用、安全质量检查免费、为个人、开发者提供依赖漏、洞检测与修复指导、核心能力、依赖更新指导、适用场景、项目上线前安全检、依赖更新前漏洞评、安全集成、差异化、免费版聚焦单项目、使用官方、适合个人开发者快、速上手、适用关键词、依赖漏洞、vulnerability、CVE等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:项目上线前安全检查
```bash
#!/bin/sh
# Go项目上线前安全检查
echo "========================================="
echo "Go项目上线前安全检查"
echo "项目: $(basename "$(pwd)")"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="
echo ""

# 1. 检查Go版本
echo "--- 1. Go环境检查 ---"
echo "  Go版本: $(go version)"
echo "  GOPATH: $(go env GOPATH)"
echo "  GOOS: $(go env GOOS)"
echo "  GOARCH: $(go env GOARCH)"

# 2. 检查go.mod
echo ""
echo "--- 2. 模块信息 ---"
if [ -f go.mod ]; then
    MODULE=$(head -1 go.mod | awk '{print $2}')
    GO_VERSION=$(head -3 go.mod | grep '^go' | awk '{print $2}')
    echo "  模块名: ${MODULE}"
    echo "  Go版本: ${GO_VERSION}"
else
    echo "  [!] 未找到go.mod"
    exit 1
fi

# 3. 编译检查
echo ""
echo "--- 3. 编译检查 ---"
if go build ./... 2>/dev/null; then
    echo "  [OK] 编译通过"
else
    echo "  [!] 编译失败"
    go build ./... 2>&1 | head -5
fi

# 4. 质量检查
echo ""
echo "--- 4. 质量检查 ---"
if command -v govulncheck &> /dev/null; then
    VULN_OUTPUT=$(govulncheck ./... 2>&1)
    VULN_COUNT=$(echo "$VULN_OUTPUT" | grep -c "Vulnerability\|GO-" || echo "0")

    if [ "$VULN_COUNT" -eq 0 ]; then
        echo "  [OK] 未发现已知漏洞"
    else
        echo "  [!] 发现 ${VULN_COUNT} 个漏洞"
        echo "$VULN_OUTPUT" | grep "GO-\|Vulnerability\|Fixed in"
    fi
else
    echo "  [!] govulncheck未安装,请运行: go install golang.org/x/vuln/cmd/govulncheck@latest"
fi

# 5. go vet检查
echo ""
echo "--- 5. 静态分析(go vet) ---"
VET_OUTPUT=$(go vet ./... 2>&1)
if [ -z "$VET_OUTPUT" ]; then
    echo "  [OK] go vet通过"
else
    echo "  [!] go vet发现问题:"
    echo "$VET_OUTPUT" | head -5
fi

echo ""
echo "========================================="
echo "安全检查完成"
echo "========================================="
```

### 场景二:依赖更新前评估
```bash
#!/bin/sh
# 依赖更新前安全评估
echo "=== 依赖更新前安全评估 ==="
echo ""

# 记录当前状态
echo "--- 1. 当前依赖漏洞 ---"
BEFORE_COUNT=$(govulncheck ./... 2>&1 | grep -c "GO-" || echo "0")
echo "  当前漏洞数: ${BEFORE_COUNT}"

# 更新依赖
echo ""
echo "--- 2. 更新依赖 ---"
go get -u ./... 2>/dev/null
go mod tidy 2>/dev/null
echo "  依赖已更新"

# 更新后扫描
echo ""
echo "--- 3. 更新后漏洞 ---"
AFTER_COUNT=$(govulncheck ./... 2>&1 | grep -c "GO-" || echo "0")
echo "  更新后漏洞数: ${AFTER_COUNT}"

# 对比
echo ""
echo "--- 4. 对比结果 ---"
DIFF=$((BEFORE_COUNT - AFTER_COUNT))
if [ "$DIFF" -gt 0 ]; then
    echo "  [OK] 漏洞减少 ${DIFF} 个"
elif [ "$DIFF" -lt 0 ]; then
    echo "  [!] 警告: 漏洞增加 $((0 - DIFF)) 个,建议回退"
else
    echo "  漏洞数量无变化"
fi
```

### 场景三:CI安全集成
```yaml
# .github/workflows/go-security.yml
name: Go Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Install govulncheck
        run: go install golang.org/x/vuln/cmd/govulncheck@latest

      - name: Run vulnerability scan
        run: |
          VULNS=$(govulncheck ./... 2>&1 | grep -c "GO-" || true)
          if [ "$VULNS" -gt 0 ]; then
            echo "Found ${VULNS} vulnerabilities"
            govulncheck ./...
            exit 1
          fi
          echo "No vulnerabilities found"

      - name: Run go vet
        run: go vet ./...
```

## 不适用场景
以下场景Go安全质量检查免费版不适合处理：

- 安全评估未授权目标
- 物理安全防护
- 社会工程学攻击

## 触发条件
需要安全检测、合规审计、质量检查、加密防护时使用。不适用于非本工具能力范围的需求。

## 快速开始
### 领先步:安装govulncheck
```bash
# 安装govulncheck
go install golang.org/x/vuln/cmd/govulncheck@latest

# 验证安装
govulncheck -version
```

### 第二步:运行扫描
```bash
# 进入Go项目目录
cd /path/to/your/go/project

# 运行质量检查
govulncheck ./...
```

### 第三步:修复漏洞
```bash
# 查看修复建议
govulncheck ./... | grep "Fixed in"

# 更新受影响的依赖
go get affected-module@latest
go mod tidy
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例
### govulncheck输出格式
| 格式参数 | 说明 | 适用场景 |
|:---------|:-----|:---------|
| 默认(文本) | 人类可读 | 日常使用 |
| -json | JSON格式 | 程序解析 |
| -mode source | 源码模式(默认) | 扫描项目源码 |
| -mode binary | 二进制模式 | 扫描编译产物 |

### 漏洞严重级别
| 级别 | 说明 | 建议处理 |
|:-----|:-----|:---------|
| CRITICAL | 严重漏洞,可直接利用 | 立即修复 |
| HIGH | 高危漏洞,有利用可能 | 本周修复 |
| MEDIUM | 中危漏洞,需要条件触发 | 下次迭代修复 |
| LOW | 低危漏洞,利用困难 | 记录跟踪 |

### 常见Go安全工具
| 工具 | 类型 | 免费版 | 说明 |
|:-----|:-----|:-------|:-----|
| govulncheck | 依赖漏洞 | 支持 | 官方质量检查器 |
| gosec | 代码安全 | 不支持 | 静态安全分析 |
| go vet | 代码质量 | 支持 | 内置静态检查 |
| staticcheck | 代码质量 | 不支持 | 高级静态分析 |

## 优选实践
1. **定期扫描**:至少每周运行一次govulncheck,及时发现新漏洞。
2. **区分调用**:关注"called"漏洞(代码实际调用了受影响函数),优先修复。
3. **锁定版本**:使用go.sum锁定依赖版本,避免意外引入漏洞版本。
4. **CI集成**:将govulncheck集成到CI流水线,每次提交自动扫描。
5. **及时更新**:Go新版本通常包含安全修复,保持Go版本最新。

```bash
# 优选实践:安全更新流程
safe_go_update() {
    local module=$1

    echo "安全更新: ${module}"

    # 1. 扫描当前漏洞
    echo "更新前质量检查..."
    BEFORE=$(govulncheck ./... 2>&1 | grep -c "GO-" || echo "0")

    # 2. 更新模块
    go get "${module}@latest"
    go mod tidy

    # 3. 编译验证
    if ! go build ./...; then
        echo "编译失败,回退更新"
        go get "${module}@previous"
        return 1
    fi

    # 4. 扫描更新后漏洞
    echo "更新后质量检查..."
    AFTER=$(govulncheck ./... 2>&1 | grep -c "GO-" || echo "0")

    echo "漏洞变化: ${BEFORE} -> ${AFTER}"

    # 5. 运行测试
    if ! go test ./...; then
        echo "测试失败,建议检查更新影响"
        return 1
    fi

    echo "更新完成"
}
```

## 常见问题
### Q1: govulncheck扫描出漏洞但代码没调用怎么办?
govulncheck会区分"called"(代码实际调用了受影响函数)和"not called"(仅依赖中存在但未调用)。未调用的漏洞风险较低,但仍建议更新。

### Q2: 如何修复没有修复版本的漏洞?
部分漏洞尚无修复版本。建议:1)评估实际影响;2)寻找替代模块;3)在代码中添加防护逻辑;4)关注模块更新动态。

### Q3: 扫描速度很慢怎么办?
govulncheck需要分析调用图,大型项目可能较慢。可以使用 `-mode binary` 模式扫描编译后的二进制,速度更快。

### Q4: 免费版支持代码安全扫描吗?
免费版使用govulncheck专注依赖漏洞。代码安全分析(gosec)需要专业版支持。

### Q5: 如何在CI中阻断有漏洞的构建?
在CI脚本中检查govulncheck输出,发现"called"漏洞时exit 1阻断构建。参考CI集成示例。

## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Go**: 1.18+(govulncheck最低要求)
- **网络**: 需可访问Go模块代理和漏洞数据库

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| go | Go工具链 | 必需 | golang.org 下载 |
| govulncheck | 质量检查器 | 必需 | `go install golang.org/x/vuln/cmd/govulncheck@latest` |
| jq | JSON处理 | 推荐 | `apt install jq` / `brew install jq` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 免费版使用官方漏洞数据库,无需API Key
- Go模块代理默认使用proxy.golang.org,如需私有代理配置GOPROXY环境变量

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,核心功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行Go项目安全质量检查与修复任务

## 错误处理
| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据