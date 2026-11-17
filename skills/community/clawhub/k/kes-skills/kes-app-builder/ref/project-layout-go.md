# Go 项目结构参考（KingbaseES）

标准的 Go + Gin + GORM 项目布局，适用于 KingbaseES 集成。

## 目录结构

```
myapp/
├── go.mod
├── go.sum
├── main.go
├── cmd/
│   └── server/
│       └── main.go              # 启动入口
├── internal/
│   ├── handler/
│   │   └── employee_handler.go  # HTTP 处理器
│   ├── service/
│   │   └── employee_service.go  # 业务逻辑
│   ├── repository/
│   │   └── employee_repo.go     # 数据访问
│   ├── model/
│   │   └── employee.go          # 数据模型
│   └── config/
│       └── config.go            # 配置加载
├── pkg/
│   └── database/
│       └── kes.go               # KingbaseES 连接
├── migrations/
│   ├── 001_init.sql
│   └── 002_add_index.sql
├── config.yaml
└── README.md
```

## go.mod 依赖

```go
module github.com/example/myapp

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/gookit/config/v2 v2.2.0
    gorm.io/gorm v1.25.5
    gorm.io/driver/postgres v1.5.3  // KingbaseES 兼容
    github.com/kingbase/gokb v1.0.0  // KingbaseES Go 驱动
)
```

## 数据库连接

```go
import (
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
    "github.com/kingbase/gokb"
)

func ConnectKES(dsn string) (*gorm.DB, error) {
    d, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
    return d, err
}
```

## config.yaml 示例

```yaml
server:
  port: 8080

database:
  host: localhost
  port: 54321
  user: SYSTEM
  password: 123456
  dbname: test
  sslmode: disable
```
