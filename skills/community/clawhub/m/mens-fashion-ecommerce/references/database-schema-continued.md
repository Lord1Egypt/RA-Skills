`start_time`,`end_time`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='优惠券表';
```

### 12. 用户优惠券表 (user_coupon)

```sql
CREATE TABLE `user_coupon` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户优惠券ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `coupon_id` bigint(20) NOT NULL COMMENT '优惠券ID',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态：1-未使用，2-已使用，3-已过期',
  `order_id` bigint(20) DEFAULT NULL COMMENT '使用的订单ID',
  `receive_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '领取时间',
  `use_time` datetime DEFAULT NULL COMMENT '使用时间',
  `expire_time` datetime NOT NULL COMMENT '过期时间',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_coupon_id` (`coupon_id`),
  KEY `idx_status` (`status`),
  KEY `idx_expire_time` (`expire_time`),
  CONSTRAINT `fk_user_coupon_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_coupon_coupon` FOREIGN KEY (`coupon_id`) REFERENCES `coupon` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户优惠券表';
```

### 13. 商品评价表 (product_review)

```sql
CREATE TABLE `product_review` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '评价ID',
  `product_id` bigint(20) NOT NULL COMMENT '商品ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `order_item_id` bigint(20) NOT NULL COMMENT '订单明细ID',
  `rating` tinyint(1) NOT NULL COMMENT '评分：1-5分',
  `content` text COMMENT '评价内容',
  `images` text COMMENT '评价图片（JSON数组）',
  `is_anonymous` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否匿名：0-否，1-是',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态：0-隐藏，1-显示',
  `like_count` int(11) NOT NULL DEFAULT '0' COMMENT '点赞数',
  `reply_count` int(11) NOT NULL DEFAULT '0' COMMENT '回复数',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_rating` (`rating`),
  KEY `idx_status` (`status`),
  KEY `idx_create_time` (`create_time`),
  CONSTRAINT `fk_review_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `fk_review_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_review_order_item` FOREIGN KEY (`order_item_id`) REFERENCES `order_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品评价表';
```

### 14. 系统配置表 (system_config)

```sql
CREATE TABLE `system_config` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `config_key` varchar(100) NOT NULL COMMENT '配置键',
  `config_value` text NOT NULL COMMENT '配置值',
  `config_name` varchar(100) NOT NULL COMMENT '配置名称',
  `config_group` varchar(50) NOT NULL COMMENT '配置分组',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_key` (`config_key`),
  KEY `idx_config_group` (`config_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';
```

## 初始数据

### 1. 初始化商品分类数据

```sql
-- 一级分类
INSERT INTO `product_category` (`parent_id`, `name`, `level`, `icon`, `sort_order`, `status`) VALUES
(0, '上衣', 1, 'icon-shirt', 1, 1),
(0, '裤装', 1, 'icon-pants', 2, 1),
(0, '外套', 1, 'icon-jacket', 3, 1),
(0, '鞋履', 1, 'icon-shoes', 4, 1),
(0, '配饰', 1, 'icon-accessories', 5, 1);

-- 上衣子分类
INSERT INTO `product_category` (`parent_id`, `name`, `level`, `sort_order`, `status`) VALUES
(1, 'T恤', 2, 1, 1),
(1, '衬衫', 2, 2, 1),
(1, 'POLO衫', 2, 3, 1),
(1, '卫衣', 2, 4, 1),
(1, '毛衣', 2, 5, 1);

-- 裤装子分类
INSERT INTO `product_category` (`parent_id`, `name`, `level`, `sort_order`, `status`) VALUES
(2, '牛仔裤', 2, 1, 1),
(2, '休闲裤', 2, 2, 1),
(2, '运动裤', 2, 3, 1),
(2, '西裤', 2, 4, 1),
(2, '短裤', 2, 5, 1);

-- 外套子分类
INSERT INTO `product_category` (`parent_id`, `name`, `level`, `sort_order`, `status`) VALUES
(3, '夹克', 2, 1, 1),
(3, '风衣', 2, 2, 1),
(3, '羽绒服', 2, 3, 1),
(3, '大衣', 2, 4, 1),
(3, '西装', 2, 5, 1);
```

### 2. 初始化系统配置数据

```sql
-- 网站配置
INSERT INTO `system_config` (`config_key`, `config_value`, `config_name`, `config_group`) VALUES
('site_name', '男装电商系统', '网站名称', 'site'),
('site_logo', '/images/logo.png', '网站Logo', 'site'),
('site_favicon', '/images/favicon.ico', '网站图标', 'site'),
('site_copyright', '© 2024 男装电商系统 版权所有', '版权信息', 'site'),
('site_icp', '京ICP备12345678号', 'ICP备案号', 'site'),

-- 商品配置
('product_default_image', '/images/default-product.jpg', '商品默认图片', 'product'),
('product_review_enabled', '1', '是否开启商品评价', 'product'),
('product_stock_warning', '10', '库存预警数量', 'product'),

-- 订单配置
('order_auto_cancel_minutes', '30', '订单自动取消时间（分钟）', 'order'),
('order_auto_confirm_days', '7', '订单自动确认收货时间（天）', 'order'),
('order_auto_complete_days', '3', '订单自动完成时间（天）', 'order'),

-- 支付配置
('payment_alipay_enabled', '1', '是否启用支付宝支付', 'payment'),
('payment_wechat_enabled', '1', '是否启用微信支付', 'payment'),
('payment_timeout_minutes', '30', '支付超时时间（分钟）', 'payment'),

-- 物流配置
('shipping_free_amount', '99', '免运费金额', 'shipping'),
('shipping_default_price', '10', '默认运费', 'shipping');
```

### 3. 初始化管理员用户

```sql
-- 管理员用户（密码：admin123）
INSERT INTO `user` (`username`, `password`, `email`, `phone`, `status`) VALUES
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTV5UiC', 'admin@mensfashion.com', '13800138000', 1);
```

## 数据库索引优化建议

### 1. 必须创建的索引

```sql
-- 商品表添加组合索引
ALTER TABLE `product` ADD INDEX `idx_category_status` (`category_id`, `status`);
ALTER TABLE `product` ADD INDEX `idx_price_sales` (`price`, `sales`);
ALTER TABLE `product` ADD INDEX `idx_create_status` (`create_time`, `status`);

-- 订单表添加组合索引
ALTER TABLE `order` ADD INDEX `idx_user_status` (`user_id`, `status`);
ALTER TABLE `order` ADD INDEX `idx_create_status` (`create_time`, `status`);
ALTER TABLE `order` ADD INDEX `idx_payment_status` (`payment_time`, `status`);

-- 购物车表添加组合索引
ALTER TABLE `cart` ADD INDEX `idx_user_selected` (`user_id`, `selected`);
ALTER TABLE `cart` ADD INDEX `idx_user_product` (`user_id`, `product_id`);

-- 用户表添加组合索引
ALTER TABLE `user` ADD INDEX `idx_status_time` (`status`, `create_time`);
```

### 2. 全文索引（用于商品搜索）

```sql
-- 为商品名称和副标题创建全文索引
ALTER TABLE `product` ADD FULLTEXT INDEX `ft_search` (`name`, `subtitle`);

-- 使用全文索引的查询示例
SELECT * FROM `product` 
WHERE MATCH(`name`, `subtitle`) AGAINST('男士衬衫' IN NATURAL LANGUAGE MODE)
AND `status` = 1
ORDER BY `sales` DESC
LIMIT 20;
```

### 3. 分区表建议（针对大数据量）

```sql
-- 订单表按创建时间分区（每月一个分区）
ALTER TABLE `order` 
PARTITION BY RANGE (YEAR(create_time) * 100 + MONTH(create_time)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    PARTITION p202403 VALUES LESS THAN (202404),
    PARTITION p202404 VALUES LESS THAN (202405),
    PARTITION p202405 VALUES LESS THAN (202406),
    PARTITION p202406 VALUES LESS THAN (202407),
    PARTITION p202407 VALUES LESS THAN (202408),
    PARTITION p202408 VALUES LESS THAN (202409),
    PARTITION p202409 VALUES LESS THAN (202410),
    PARTITION p202410 VALUES LESS THAN (202411),
    PARTITION p202411 VALUES LESS THAN (202412),
    PARTITION p202412 VALUES LESS THAN (202501),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- 订单明细表按订单ID哈希分区
ALTER TABLE `order_item`
PARTITION BY HASH(order_id)
PARTITIONS 8;
```

## 数据库维护脚本

### 1. 数据库备份脚本

```bash
#!/bin/bash
# backup.sh - 数据库备份脚本

# 配置
DB_HOST="localhost"
DB_PORT="3306"
DB_USER="root"
DB_PASS="your_password"
DB_NAME="mens_fashion_db"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE}.sql"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASS \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  $DB_NAME > $BACKUP_FILE

# 压缩备份文件
gzip $BACKUP_FILE

# 删除7天前的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "备份完成: ${BACKUP_FILE}.gz"
```

### 2. 数据库优化脚本

```sql
-- 优化表
OPTIMIZE TABLE `order`, `order_item`, `product`, `user`;

-- 分析表（更新索引统计信息）
ANALYZE TABLE `order`, `order_item`, `product`, `user`;

-- 修复表（如果表损坏）
REPAIR TABLE `order`, `order_item`, `product`, `user`;

-- 清理过期数据（保留最近3个月的订单）
DELETE FROM `order` 
WHERE `status` IN (4, 5, 6) 
AND `create_time` < DATE_SUB(NOW(), INTERVAL 3 MONTH);

-- 清理购物车过期数据（30天未更新）
DELETE FROM `cart` 
WHERE `update_time` < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

### 3. 监控查询

```sql
-- 查看慢查询
SELECT * FROM mysql.slow_log 
WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 DAY)
ORDER BY query_time DESC
LIMIT 10;

-- 查看锁等待
SELECT * FROM information_schema.INNODB_LOCKS;
SELECT * FROM information_schema.INNODB_LOCK_WAITS;

-- 查看连接数
SHOW STATUS LIKE 'Threads_connected';
SHOW PROCESSLIST;

-- 查看表大小
SELECT 
    table_schema as '数据库',
    table_name as '表名',
    round(((data_length + index_length) / 1024 / 1024), 2) as '大小(MB)'
FROM information_schema.TABLES
WHERE table_schema = 'mens_fashion_db'
ORDER BY (data_length + index_length) DESC;
```

## 数据库安全建议

### 1. 用户权限管理

```sql
-- 创建应用用户（只授予必要权限）
CREATE USER 'app_user'@'%' IDENTIFIED BY 'StrongPassword123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON mens_fashion_db.* TO 'app_user'@'%';
GRANT EXECUTE ON mens_fashion_db.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

-- 创建只读用户（用于报表查询）
CREATE USER 'report_user'@'%' IDENTIFIED BY 'ReadOnlyPassword123!';
GRANT SELECT ON mens_fashion_db.* TO 'report_user'@'%';
FLUSH PRIVILEGES;
```

### 2. 数据加密

```sql
-- 使用AES加密敏感数据
INSERT INTO `user` (`username`, `password`, `email`, `phone`) VALUES
('user1', 
 AES_ENCRYPT('password123', 'encryption_key'),
 AES_ENCRYPT('user1@example.com', 'encryption_key'),
 AES_ENCRYPT('13800138001', 'encryption_key')
);

-- 查询时解密
SELECT 
    `username`,
    AES_DECRYPT(`password`, 'encryption_key') as `password`,
    AES_DECRYPT(`email`, 'encryption_key') as `email`,
    AES_DECRYPT(`phone`, 'encryption_key') as `phone`
FROM `user`;
```

### 3. 审计日志

```sql
-- 创建审计表
CREATE TABLE `audit_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT NULL,
  `action` varchar(100) NOT NULL,
  `table_name` varchar(100) NOT NULL,
  `record_id` bigint(20) DEFAULT NULL,
  `old_data` json DEFAULT NULL,
  `new_data` json DEFAULT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `user_agent` text,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_action` (`action`),
  KEY `idx_table_name` (`table_name`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='审计日志表';
```

这个数据库设计提供了完整的男装电商系统所需的所有表结构，包括用户管理、商品管理、订单管理、支付管理、库存管理等核心功能。设计考虑了性能优化、数据安全和可扩展性，适合生产环境使用。