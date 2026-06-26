package main

import (
	"database/sql"
	"fmt"
	"math/rand"
	"net/http"
	"os"
	"time"
)

// 不安全随机数示例
func generateToken() string {
	rand.Seed(time.Now().UnixNano()) // 风险: 使用 math/rand
	return fmt.Sprintf("%x", rand.Intn(1000000))
}

// SQL 注入风险
func queryUser(db *database.DB, username string) {
	query := "SELECT * FROM users WHERE username = '" + username + "'" // 风险: SQL注入
	db.Query(query)
}

// 硬编码凭证
const API_KEY = "sk-1234567890abcdef" // 风险: 硬编码密钥

// 敏感文件系统访问
func readSensitive() {
	os.Open("/etc/shadow") // 风险: 访问敏感文件
}

// 未使用 HTTPS
func serve() {
	http.ListenAndServe(":80", nil) // 风险: 未使用 HTTPS
}

func main() {
	token := generateToken()
	fmt.Println("Token:", token)
}
