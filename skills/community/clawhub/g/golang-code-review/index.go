#!/usr/bin/env go
//go:build ignore

package main

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

var (
	// 严重级别定义
	errorLevel       = "🔴 严重"
	warningLevel     = "⚠️ 警告"
	noteLevel        = "💡 提示"
	
	// 规则配置
	rulesConfig = map[string]string{
		"go-fmt":         "代码格式必须使用 gofmt/goimports",
		"no-unused-imp":  "移除未使用的导入",
		"no-var-naming":  "变量命名不能与关键字冲突",
		"defer-placement": "defer 语句应放在函数顶部",
		"error-checking": "错误必须检查并处理",
		"magic-numbers":  "避免魔术数字，使用常量",
		"max-line-length": "单行长度不超过 120 个字符",
		"func-length":    "函数不宜过长（建议<100 行）",
		"too-many-params": "参数不应超过 4-5 个",
		"deep-nesting":   "避免深层嵌套",
		"no-global-var":  "避免全局变量",
		"doc-comments":   "函数必须添加注释",
	}
)

type Issue struct {
	Severity string
	Rule     string
	Line     int
	Message  string
}

type Report struct {
	Filename      string
	TotalIssues   int
	CriticalCount int
	WarningCount  int
	NoteCount     int
	Issues        []Issue
	Metrics       Metrics
}

type Metrics struct {
	FileSize         int64
	LineCount        int
	FuncCount        int
	ComplexityAvg    float64
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("用法：golang-code-review <提交路径或目录>")
		os.Exit(1)
	}

	path := os.Args[1]
	report := analyzeGoCode(path)
	generateReport(report)
}

// 分析 Go 代码文件
func analyzeGoCode(path string) *Report {
	var issues []Issue
	metrics := Metrics{
		FileSize:   0,
		LineCount:  0,
		FuncCount:  0,
		ComplexityAvg: 0,
	}

	// 读取文件内容
	content, err := os.ReadFile(path)
	if err != nil {
		fmt.Printf("读取文件失败：%v\n", err)
		return &Report{}
	}

	metrics.FileSize = int64(len(content))
	lines := strings.Split(string(content), "\n")
	metrics.LineCount = len(lines)

	// 执行代码审查规则检查
	for rule, message := range rulesConfig {
		issues = append(issues, checkRule(rule, string(content), lines, path, metrics))
	}

	return &Report{
		Filename:   filepath.Base(path),
		TotalIssues: len(issues),
		CriticalCount: countSeverity(issues, errorLevel),
		WarningCount: countSeverity(issues, warningLevel),
		NoteCount:    countSeverity(issues, noteLevel),
		Issues:       issues,
		Metrics:      metrics,
	}
}

// 检查特定规则
func checkRule(rule, content string, lines []string, filename string, metrics Metrics) Issue {
	// 简单实现示例，根据 rule 名称执行相应检查
	switch rule {
	case "go-fmt":
		return checkFormat(content)
	case "no-unused-imp":
		return checkUnusedImports(content)
	case "error-checking":
		return checkErrorHandling(content, lines)
	}
	
	return Issue{}
}

// 检查代码格式
func checkFormat(content string) Issue {
	// 使用 gofmt 或简单正则检查基本格式
	// 这里简化实现
	return Issue{
		Severity: noteLevel,
		Rule:     "go-fmt",
		Line:     1,
		Message:  "建议运行 'gofmt -w' 进行代码格式化",
	}
}

// 检查未使用导入
func checkUnusedImports(content string) Issue {
	// 解析 imports 块，检测未使用的导入
	importPattern := regexp.MustCompile(`^\s*import\s+\((.*)\)$`)
	match := importPattern.FindStringSubmatch(content)
	if len(match) > 1 {
		imports := match[1]
		// 检查是否包含未使用的导入
		return Issue{
			Severity: noteLevel,
			Rule:     "no-unused-imp",
			Line:     0,
			Message:  "请检查并移除未使用的导入（使用 'goimports -w' 自动修复）",
		}
	}
	
	return Issue{}
}

// 检查错误处理
func checkErrorHandling(content string, lines []string) Issue {
	// 简化实现，实际项目应使用更复杂的静态分析
	for i, line := range lines {
		// 检测未处理的错误赋值（如 err = ...; 但没有检查）
		if strings.Contains(line, "err =") && !strings.Contains(line, "if err") && !strings.Contains(line, "switch err") {
			return Issue{
				Severity: errorLevel,
				Rule:     "error-checking",
				Line:     i + 1,
				Message:  fmt.Sprintf("第 %d 行：错误赋值后未检查，请添加错误处理逻辑", i+1),
				}
			} 
		}
	}
	return Issue{}
}

func countSeverity(issues []Issue, severity string) int {
	count := 0
	for _, issue := range issues {
		if issue.Severity == severity {
			count++
			}
		}
	return count
}

// 生成报告
func generateReport(report *Report) {
	fmt.Println("======================================")
	fmt.Println("🐛 Golang 代码审查报告")
	fmt.Println("======================================")
	fmt.Printf("📄 文件：%s\n", report.Filename)
	fmt.Printf("📊 总问题数：%d\n", report.TotalIssues)
	fmt.Printf("%s %d 个\n", errorLevel, report.CriticalCount)
	fmt.Printf("%s %d 个\n", warningLevel, report.WarningCount)
	fmt.Printf("%s %d 个\n", noteLevel, report.NoteCount)
	fmt.Println("======================================")
	
	// 按严重级别排序输出问题
	if len(report.Issues) > 0 {
		sort.Slice(report.Issues, func(i, j int) bool {
			priority := map[string]int{
				errorLevel:       1,
				warningLevel:      2,
				noteLevel:         3,
				}
			return priority[report.Issues[i].Severity] < priority[report.Issues[j].Severity]
			})

		for _, issue := range report.Issues {
			fmt.Printf("\n%s [%s]\n", issue.Severity, issue.Rule)
			fmt.Printf("📍 第 %d 行：%s\n", issue.Line, issue.Message)
			}
		} else {
			fmt.Println("✅ 未发现明显问题！")
			}

		// 添加度量信息
		fmt.Printf("\n======================================\n")
		fmt.Println("📊 代码度量：")
		fmt.Printf("📏 文件大小：%d 字节\n", report.Metrics.FileSize)
		fmt.Printf("📝 代码行数：%d 行\n", report.Metrics.LineCount)
		fmt.Printf("🎯 平均复杂度：%f\n", report.Metrics.ComplexityAvg)
		fmt.Println("======================================")
}