package main

import (
	"bytes"
	"crypto/tls"
	"encoding/base64"
	"fmt"
	"io"
	"log"
	"net"
	"net/smtp"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// MailConfig 邮件配置
type MailConfig struct {
	SMTPHost string
	SMTPPort string
	Username string
	Password string
	From     string
	FromName string
}

// Email 邮件结构
type Email struct {
	To      []string
	Subject string
	Body    string // HTML content
	Files   []string
}

// NewMailConfig 从环境变量创建配置
func NewMailConfig() *MailConfig {
	return &MailConfig{
		SMTPHost: getEnv("SMTP_HOST", "smtp.qq.com"),
		SMTPPort: getEnv("SMTP_PORT", "587"),
		Username: getEnv("SMTP_USERNAME", ""),
		Password: getEnv("SMTP_PASSWORD", ""),
		From:     getEnv("FROM_EMAIL", ""),
		FromName: getEnv("FROM_NAME", "Agent通知系统"),
	}
}

// getEnv 获取环境变量，带默认值
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

// Send 发送邮件
func (e *Email) Send(config *MailConfig) error {
	// 构建 MIME 边界
	boundary := generateBoundary()

	// 构建邮件头
	var msg bytes.Buffer
	msg.WriteString(fmt.Sprintf("From: %s <%s>\r\n", config.FromName, config.From))
	msg.WriteString(fmt.Sprintf("To: %s\r\n", strings.Join(e.To, ", ")))
	msg.WriteString(fmt.Sprintf("Subject: %s\r\n", e.Subject))
	msg.WriteString(fmt.Sprintf("MIME-Version: 1.0\r\n"))

	if len(e.Files) > 0 {
		msg.WriteString(fmt.Sprintf("Content-Type: multipart/mixed; boundary=\"%s\"\r\n", boundary))
	} else {
		msg.WriteString("Content-Type: text/html; charset=\"UTF-8\"\r\n")
	}
	msg.WriteString("\r\n")

	// 如果没有附件，直接发送 HTML
	if len(e.Files) == 0 {
		msg.WriteString(e.Body)
	} else {
		// 有附件，使用 multipart
		msg.WriteString(fmt.Sprintf("--%s\r\n", boundary))
		msg.WriteString("Content-Type: text/html; charset=\"UTF-8\"\r\n\r\n")
		msg.WriteString(e.Body)
		msg.WriteString("\r\n")

		// 添加附件
		for _, file := range e.Files {
			if err := addAttachment(&msg, file, boundary); err != nil {
				return fmt.Errorf("failed to attach %s: %w", file, err)
			}
		}
		msg.WriteString(fmt.Sprintf("--%s--\r\n", boundary))
	}

	// 使用 STARTTLS 发送邮件
	return sendMailWithSTARTTLS(config, e.To, msg.Bytes())
}

// sendMailWithSTARTTLS 使用 STARTTLS 发送邮件
func sendMailWithSTARTTLS(config *MailConfig, to []string, msg []byte) error {
	addr := fmt.Sprintf("%s:%s", config.SMTPHost, config.SMTPPort)

	// 先建立普通 TCP 连接
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		return fmt.Errorf("connection failed: %w", err)
	}
	defer conn.Close()

	client, err := smtp.NewClient(conn, config.SMTPHost)
	if err != nil {
		return fmt.Errorf("smtp client creation failed: %w", err)
	}
	defer client.Close()

	// 发送 EHLO
	if err := client.Hello("localhost"); err != nil {
		return fmt.Errorf("ehlo failed: %w", err)
	}

	// 检查服务器是否支持 STARTTLS，然后升级
	if ok, _ := client.Extension("STARTTLS"); ok {
		if err := client.StartTLS(&tls.Config{
			ServerName: config.SMTPHost,
		}); err != nil {
			return fmt.Errorf("starttls failed: %w", err)
		}
	}

	// 认证
	auth := smtp.PlainAuth("", config.Username, config.Password, config.SMTPHost)
	if err := client.Auth(auth); err != nil {
		return fmt.Errorf("authentication failed: %w", err)
	}

	// 设置发件人
	if err := client.Mail(config.From); err != nil {
		return fmt.Errorf("set sender failed: %w", err)
	}

	// 设置收件人
	for _, recipient := range to {
		if err := client.Rcpt(recipient); err != nil {
			return fmt.Errorf("set recipient failed: %w", err)
		}
	}

	// 发送邮件内容
	writer, err := client.Data()
	if err != nil {
		return fmt.Errorf("data command failed: %w", err)
	}
	defer writer.Close()

	_, err = writer.Write(msg)
	if err != nil {
		return fmt.Errorf("send body failed: %w", err)
	}

	log.Printf("✅ 邮件发送成功：到 %v, 主题：%s", to, getSubject(msg))
	return nil
}

// getSubject 从邮件内容中提取主题
func getSubject(msg []byte) string {
	lines := strings.Split(string(msg), "\r\n")
	for _, line := range lines {
		if strings.HasPrefix(line, "Subject: ") {
			return strings.TrimPrefix(line, "Subject: ")
		}
	}
	return "(无主题)"
}

// addAttachment 添加附件
func addAttachment(w io.Writer, filePath, boundary string) error {
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	fileName := filepath.Base(filePath)

	w.Write([]byte(fmt.Sprintf("--%s\r\n", boundary)))
	w.Write([]byte("Content-Type: application/octet-stream\r\n"))
	w.Write([]byte(fmt.Sprintf("Content-Disposition: attachment; filename=\"%s\"\r\n", fileName)))
	w.Write([]byte("Content-Transfer-Encoding: base64\r\n\r\n"))

	encoder := base64.NewEncoder(base64.StdEncoding, w)
	defer encoder.Close()

	_, err = io.Copy(encoder, file)
	return err
}

// generateBoundary 生成 MIME 边界
func generateBoundary() string {
	return fmt.Sprintf("=%s=", url.QueryEscape(os.Getenv("HOSTNAME")))
}

// TestConnection 测试 SMTP 连接
func TestConnection(config *MailConfig) error {
	addr := fmt.Sprintf("%s:%s", config.SMTPHost, config.SMTPPort)

	// 先建立普通 TCP 连接
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		return fmt.Errorf("connection failed: %w", err)
	}
	defer conn.Close()

	client, err := smtp.NewClient(conn, config.SMTPHost)
	if err != nil {
		return fmt.Errorf("smtp client creation failed: %w", err)
	}
	defer client.Close()

	// 发送 EHLO
	if err := client.Hello("localhost"); err != nil {
		return fmt.Errorf("ehlo failed: %w", err)
	}

	// 检查服务器是否支持 STARTTLS，然后升级
	if ok, _ := client.Extension("STARTTLS"); ok {
		if err := client.StartTLS(&tls.Config{
			ServerName: config.SMTPHost,
		}); err != nil {
			return fmt.Errorf("starttls failed: %w", err)
		}
	}

	// 认证
	auth := smtp.PlainAuth("", config.Username, config.Password, config.SMTPHost)
	if err := client.Auth(auth); err != nil {
		return fmt.Errorf("authentication failed: %w", err)
	}

	log.Println("✅ SMTP 连接测试成功")
	return nil
}

func main() {
	// 解析命令参数
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	switch os.Args[1] {
	case "test":
		testConnection()
	case "send":
		sendEmail()
	default:
		printUsage()
	}
}

func printUsage() {
	fmt.Println(`Go 邮件发送工具
使用方法：
  mail_sender test              - 测试 SMTP 连接
  mail_sender send              - 发送邮件

环境变量配置：
  SMTP_HOST     - SMTP 服务器地址 (默认：smtp.qq.com)
  SMTP_PORT     - SMTP 端口 (默认：587)
  SMTP_USERNAME - 发件邮箱
  SMTP_PASSWORD - 授权码
  FROM_EMAIL    - 发件人邮箱
  FROM_NAME     - 发件人名称`)
}

func testConnection() {
	config := NewMailConfig()
	if err := TestConnection(config); err != nil {
		log.Printf("❌ 测试失败：%v", err)
		os.Exit(1)
	}
}

func sendEmail() {
	config := NewMailConfig()

	// 示例邮件
	email := &Email{
		To:      []string{"siysun@outlook.com"},
		Subject: "[Agent 测试] 邮件发送功能验证",
		Body: `
<html>
<body>
<h2>👁️ 邮件发送成功</h2>
<p>这是 Go 语言实现的 SMTP 邮件发送工具的测试邮件。</p>
<p>时间：` + getCurrentTime() + `</p>
</body>
</html>`,
	}

	if err := email.Send(config); err != nil {
		log.Printf("❌ 发送失败：%v", err)
		os.Exit(1)
	}
}

func getCurrentTime() string {
	return time.Now().Format("2006-01-02 15:04:05 CST")
}
