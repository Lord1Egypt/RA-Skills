#!/bin/bash

# 男装电商系统项目生成脚本
# 生成完整的SpringBoot3 + Vue3 + MySQL电商系统

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目配置
PROJECT_NAME="mens-fashion-ecommerce"
BACKEND_DIR="${PROJECT_NAME}-backend"
FRONTEND_DIR="${PROJECT_NAME}-frontend"
DATABASE_NAME="mens_fashion_db"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    print_info "检查系统依赖..."
    
    # 检查Java
    if ! command -v java &> /dev/null; then
        print_error "Java未安装，请先安装Java 17或更高版本"
        exit 1
    fi
    
    java_version=$(java -version 2>&1 | head -n 1 | awk -F '"' '{print $2}')
    print_info "Java版本: $java_version"
    
    # 检查Maven
    if ! command -v mvn &> /dev/null; then
        print_error "Maven未安装，请先安装Maven 3.8+"
        exit 1
    fi
    
    mvn_version=$(mvn -v | grep "Apache Maven" | awk '{print $3}')
    print_info "Maven版本: $mvn_version"
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js未安装，请先安装Node.js 16+"
        exit 1
    fi
    
    node_version=$(node --version)
    print_info "Node.js版本: $node_version"
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        print_error "npm未安装"
        exit 1
    fi
    
    npm_version=$(npm --version)
    print_info "npm版本: $npm_version"
    
    # 检查MySQL
    if ! command -v mysql &> /dev/null; then
        print_warning "MySQL未安装，数据库初始化步骤将跳过"
    else
        mysql_version=$(mysql --version | awk '{print $5}')
        print_info "MySQL版本: $mysql_version"
    fi
    
    print_success "依赖检查完成"
}

# 创建项目目录结构
create_project_structure() {
    print_info "创建项目目录结构..."
    
    # 创建主项目目录
    mkdir -p "$PROJECT_NAME"
    cd "$PROJECT_NAME"
    
    # 创建后端项目结构
    print_info "创建后端项目结构..."
    mkdir -p "$BACKEND_DIR"/src/main/java/com/mensfashion/ecommerce/{config,controller/{auth,user,product,cart,order,payment,admin},service/impl,mapper,entity,dto/{request,response},vo,enums,exception,utils}
    mkdir -p "$BACKEND_DIR"/src/main/resources/{mapper,static,templates}
    mkdir -p "$BACKEND_DIR"/src/test/java/com/mensfashion/ecommerce
    
    # 创建前端项目结构
    print_info "创建前端项目结构..."
    mkdir -p "$FRONTEND_DIR"/src/{api,assets/{images,styles,fonts},components/{common,layout,business},composables,router,store/modules,utils,views/{auth,product,cart,order,user,admin,error}}
    
    # 创建文档目录
    mkdir -p docs/{api,database,deployment}
    
    # 创建脚本目录
    mkdir -p scripts
    
    print_success "项目目录结构创建完成"
}

# 生成后端项目文件
generate_backend_files() {
    print_info "生成后端项目文件..."
    
    cd "$BACKEND_DIR"
    
    # 1. 生成pom.xml
    cat > pom.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.1.5</version>
        <relativePath/>
    </parent>

    <groupId>com.mensfashion</groupId>
    <artifactId>ecommerce-backend</artifactId>
    <version>1.0.0</version>
    <name>mens-fashion-ecommerce-backend</name>
    <description>男装电商系统后端</description>

    <properties>
        <java.version>17</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <mybatis-plus.version>3.5.4</mybatis-plus.version>
        <jjwt.version>0.11.5</jjwt.version>
        <fastjson.version>2.0.42</fastjson.version>
        <hutool.version>5.8.22</hutool.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Starters -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-aop</artifactId>
        </dependency>

        <!-- Database -->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>${mybatis-plus.version}</version>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
            <version>1.2.18</version>
        </dependency>

        <!-- JWT -->
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>${jjwt.version}</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>

        <!-- JSON -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>${fastjson.version}</version>
        </dependency>

        <!-- Utils -->
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>${hutool.version}</version>
        </dependency>

        <!-- API Documentation -->
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>2.2.0</version>
        </dependency>

        <!-- Development Tools -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
EOF

    # 2. 生成application.yml
    cat > src/main/resources/application.yml << 'EOF'
spring:
  application:
    name: mens-fashion-ecommerce

  # 数据源配置
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/mens_fashion_db?useUnicode=true&characterEncoding=utf-8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456
    type: com.alibaba.druid.pool.DruidDataSource
    druid:
      initial-size: 5
      min-idle: 5
      max-active: 20
      max-wait: 60000
      time-between-eviction-runs-millis: 60000
      min-evictable-idle-time-millis: 300000
      validation-query: SELECT 1
      test-while-idle: true
      test-on-borrow: false
      test-on-return: false
      pool-prepared-statements: true
      max-pool-prepared-statement-per-connection-size: 20
      filters: stat,wall,slf4j
      connection-properties: druid.stat.mergeSql=true;druid.stat.slowSqlMillis=5000

  # Redis配置
  redis:
    host: localhost
    port: 6379
    password:
    database: 0
    timeout: 3000ms
    lettuce:
      pool:
        max-active: 20
        max-idle: 10
        min-idle: 5
        max-wait: 3000ms

  # Jackson配置
  jackson:
    date-format: yyyy-MM-dd HH:mm:ss
    time-zone: Asia/Shanghai
    serialization:
      write-dates-as-timestamps: false

  # 文件上传配置
  servlet:
    multipart:
      max-file-size: 10MB
      max-request-size: 100MB

# MyBatis Plus配置
mybatis-plus:
  configuration:
    map-underscore-to-camel-case: true
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  global-config:
    db-config:
      id-type: auto
      logic-delete-field: deleted
      logic-delete-value: 1
      logic-not-delete-value: 0

# JWT配置
jwt:
  secret: mens-fashion-ecommerce-secret-key-2024
  expiration: 7200
  header: Authorization

# 应用配置
app:
  upload:
    path: ./uploads
    max-size: 10MB
    allowed-types: jpg,jpeg,png,gif
  cors:
    allowed-origins: http://localhost:3000
    allowed-methods: GET,POST,PUT,DELETE,OPTIONS
    allowed-headers: "*"
    allow-credentials: true

# 日志配置
logging:
  level:
    com.mensfashion.ecommerce: debug
    org.springframework.security: debug
  file:
    name: logs/app.log
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"

# 服务器配置
server:
  port: 8080
  servlet:
    context-path: /
  compression:
    enabled: true
    mime-types: text/html,text/xml,text/plain,text/css,text/javascript,application/javascript,application/json
    min-response-size: 1024
EOF

    # 3. 生成启动类
    cat > src/main/java/com/mensfashion/ecommerce/EcommerceApplication.java << 'EOF'
package com.mensfashion.ecommerce;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@MapperScan("com.mensfashion.ecommerce.mapper")
@EnableCaching
@EnableAsync
@EnableScheduling
public class EcommerceApplication {
    public static void main(String[] args) {
        SpringApplication.run(EcommerceApplication.class, args);
    }
}
EOF

    # 4. 生成统一响应类
    cat > src/main/java/com/mensfashion/ecommerce/dto/response/Result.java << 'EOF'
package com.mensfashion.ecommerce.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Result<T> implements Serializable {
    
    private Integer code;
    private String message;
    private T data;
    private Long timestamp;
    
    public static <T> Result<T> success() {
        return new Result<>(200, "success", null, System.currentTimeMillis());
    }
    
    public static <T> Result<T> success(T data) {
        return new Result<>(200, "success", data, System.currentTimeMillis());
    }
    
    public static <T> Result<T> success(String message, T data) {
        return new Result<>(200, message, data, System.currentTimeMillis());
    }
    
    public static <T> Result<T> error(Integer code, String message) {
        return new Result<>(code, message, null, System.currentTimeMillis());
    }
    
    public static <T> Result<T> error(String message) {
        return new Result<>(500, message, null, System.currentTimeMillis());
    }
    
    public static <T> Result<T> error() {
        return new Result<>(500, "系统异常", null, System.currentTimeMillis());
    }
}
EOF

    # 5. 生成业务异常类
    cat > src/main/java/com/mensfashion/ecommerce/exception/BusinessException.java << 'EOF'
package com.mensfashion.ecommerce.exception;

import lombok.Getter;

@Getter
public class BusinessException extends RuntimeException {
    
    private final Integer code;
    
    public BusinessException(String message) {
        super(message);
        this.code = 500;
    }
    
    public BusinessException(Integer code, String message) {
        super(message);
        this.code = code;
    }
    
    public BusinessException(String message, Throwable cause) {
        super(message, cause);
        this.code = 500;
    }
    
    public BusinessException(Integer code, String message, Throwable cause) {
        super(message, cause);
        this.code = code;
    }
}
EOF

    print_success "后端项目文件生成完成"
    cd ..
}

# 生成前端项目文件
generate_frontend_files() {
    print_info "生成前端项目文件..."
    
    cd "$FRONTEND_DIR"
    
    # 1. 生成package.json
    cat > package.json << 'EOF'
{
  "name": "mens-fashion-ecommerce-frontend",
  "version": "1.0.0",
  "description": "男装电商系统前端",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix",
    "format": "prettier --write src/"
  },
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2",
    "element-plus": "^2.4.1",
    "@element-plus/icons-vue