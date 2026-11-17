-- UUIDv7 示例
-- INSERT 示例：INSERT INTO t(id, ...) VALUES (UUID_TO_BIN(UUID(), true), ...);
-- 备注：生产建议使用服务端生成UUIDv7并传入。

-- 审计列模板
`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
`created_by` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '创建人',
`updated_by` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '更新人',
`deleted_at` DATETIME NULL DEFAULT NULL COMMENT '删除时间',

-- 软删除过滤推荐索引
KEY `idx_{table}_not_deleted` (`deleted_at`)
