# 常见业务场景设计模式

## 1. 用户认证与权限

### 数据表

```sql
-- 用户表
CREATE TABLE `user` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(64) NOT NULL COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT '密码哈希',
    `email` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '邮箱',
    `phone` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '手机号',
    `avatar` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '头像URL',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 0-禁用 1-启用',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` DATETIME DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    UNIQUE KEY `uk_email` (`email`),
    UNIQUE KEY `uk_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 角色表
CREATE TABLE `role` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL COMMENT '角色名称',
    `code` VARCHAR(64) NOT NULL COMMENT '角色编码',
    `description` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '描述',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- 用户角色关联表
CREATE TABLE `user_role` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `role_id` BIGINT UNSIGNED NOT NULL COMMENT '角色ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_role` (`user_id`, `role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户角色关联表';
```

### Proto 接口

```protobuf
service AuthService {
    rpc Register(RegisterRequest) returns (RegisterResponse);
    rpc Login(LoginRequest) returns (LoginResponse);
    rpc Logout(LogoutRequest) returns (LogoutResponse);
    rpc RefreshToken(RefreshTokenRequest) returns (RefreshTokenResponse);
}

message LoginRequest {
    string username = 1;
    string password = 2;
}

message LoginResponse {
    string access_token = 1;
    string refresh_token = 2;
    int64 expires_in = 3;
    User user = 4;
}
```

---

## 2. 订单系统

### 数据表

```sql
-- 订单主表
CREATE TABLE `order` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订单ID',
    `order_no` VARCHAR(64) NOT NULL COMMENT '订单编号',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `total_amount` DECIMAL(20,2) NOT NULL COMMENT '订单总金额',
    `pay_amount` DECIMAL(20,2) NOT NULL COMMENT '实付金额',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '状态: 0-待支付 1-已支付 2-已发货 3-已完成 4-已取消 5-已退款',
    `payment_method` TINYINT NOT NULL DEFAULT 0 COMMENT '支付方式: 0-未知 1-微信 2-支付宝 3-银行卡',
    `payment_time` DATETIME DEFAULT NULL COMMENT '支付时间',
    `remark` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '备注',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` DATETIME DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_order_no` (`order_no`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_status` (`status`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 订单明细表
CREATE TABLE `order_item` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_id` BIGINT UNSIGNED NOT NULL COMMENT '订单ID',
    `product_id` BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
    `product_name` VARCHAR(255) NOT NULL COMMENT '商品名称',
    `sku_id` BIGINT UNSIGNED NOT NULL COMMENT 'SKU ID',
    `quantity` INT UNSIGNED NOT NULL COMMENT '数量',
    `unit_price` DECIMAL(20,2) NOT NULL COMMENT '单价',
    `total_price` DECIMAL(20,2) NOT NULL COMMENT '小计',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_order_id` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单明细表';
```

### Proto 接口

```protobuf
service OrderService {
    rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);
    rpc GetOrder(GetOrderRequest) returns (GetOrderResponse);
    rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);
    rpc CancelOrder(CancelOrderRequest) returns (CancelOrderResponse);
    rpc PayOrder(PayOrderRequest) returns (PayOrderResponse);
}

message CreateOrderRequest {
    repeated OrderItem items = 1;
    string remark = 2;
    int32 payment_method = 3;
}

message OrderItem {
    int64 product_id = 1;
    int64 sku_id = 2;
    int32 quantity = 3;
}

message CreateOrderResponse {
    Order order = 1;
}
```

---

## 3. 商品与库存

### 数据表

```sql
-- 商品表
CREATE TABLE `product` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT '商品名称',
    `category_id` BIGINT UNSIGNED NOT NULL COMMENT '分类ID',
    `brand_id` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '品牌ID',
    `description` TEXT COMMENT '商品描述',
    `price` DECIMAL(20,2) NOT NULL COMMENT '售价',
    `original_price` DECIMAL(20,2) NOT NULL COMMENT '原价',
    `stock` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '库存',
    `sales` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '销量',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 0-下架 1-上架',
    `sort` INT NOT NULL DEFAULT 0 COMMENT '排序',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` DATETIME DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_category_id` (`category_id`),
    KEY `idx_status_sort` (`status`, `sort`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- SKU表
CREATE TABLE `product_sku` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `product_id` BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
    `sku_code` VARCHAR(64) NOT NULL COMMENT 'SKU编码',
    `specs` JSON COMMENT '规格属性: {"颜色": "红色", "尺寸": "L"}',
    `price` DECIMAL(20,2) NOT NULL COMMENT '售价',
    `stock` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '库存',
    `image` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '图片',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_sku_code` (`sku_code`),
    KEY `idx_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品SKU表';
```

---

## 4. 内容管理

### 数据表

```sql
-- 文章表
CREATE TABLE `article` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL COMMENT '标题',
    `author_id` BIGINT UNSIGNED NOT NULL COMMENT '作者ID',
    `category_id` BIGINT UNSIGNED NOT NULL COMMENT '分类ID',
    `summary` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '摘要',
    `content` LONGTEXT COMMENT '内容',
    `cover` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '封面图',
    `view_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '浏览量',
    `like_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '点赞数',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '状态: 0-草稿 1-已发布 2-已下架',
    `published_at` DATETIME DEFAULT NULL COMMENT '发布时间',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` DATETIME DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_author_id` (`author_id`),
    KEY `idx_category_id` (`category_id`),
    KEY `idx_status_published` (`status`, `published_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章表';
```

---

## 5. 日志与审计

### 数据表

```sql
-- 操作日志表
CREATE TABLE `operation_log` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '操作用户ID',
    `username` VARCHAR(64) NOT NULL COMMENT '用户名',
    `module` VARCHAR(64) NOT NULL COMMENT '模块',
    `action` VARCHAR(64) NOT NULL COMMENT '操作',
    `target_type` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '目标类型',
    `target_id` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '目标ID',
    `request_data` JSON COMMENT '请求数据',
    `response_code` INT NOT NULL DEFAULT 0 COMMENT '响应码',
    `ip` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'IP地址',
    `user_agent` VARCHAR(512) NOT NULL DEFAULT '' COMMENT 'User-Agent',
    `duration` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '耗时(ms)',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_module_action` (`module`, `action`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';
```

---

## 命名速查

| 类型 | 规范 | 示例 |
|------|------|------|
| 表名 | 蛇形小写 | `user_order` |
| 字段名 | 蛇形小写 | `created_at` |
| 索引 | `idx_` 前缀 | `idx_user_id` |
| 唯一索引 | `uk_` 前缀 | `uk_order_no` |
| Proto package | `api.{module}.v1` | `api.user.v1` |
| Service | 大驼峰 | `UserService` |
| Method | 动词+名词 | `CreateUser` |
| Message | 名词+类型 | `UserRequest` |
