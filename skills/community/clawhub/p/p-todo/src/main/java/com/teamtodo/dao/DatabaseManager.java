package com.teamtodo.dao;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class DatabaseManager {
    private static final Logger log = LoggerFactory.getLogger(DatabaseManager.class);
    private static DatabaseManager instance;
    private final HikariDataSource dataSource;

    private DatabaseManager(String dbPath) {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:sqlite:" + dbPath);
        config.setMaximumPoolSize(5);
        config.setMinimumIdle(1);
        config.setConnectionTimeout(10000);
        config.setLeakDetectionThreshold(30000);
        this.dataSource = new HikariDataSource(config);
        initTables();
        log.info("数据库已连接: {}", dbPath);
    }

    public static synchronized DatabaseManager getInstance(String dbPath) {
        if (instance == null) {
            instance = new DatabaseManager(dbPath);
        }
        return instance;
    }

    public static DatabaseManager getInstance() {
        if (instance == null) {
            throw new IllegalStateException("数据库未初始化，请先调用 getInstance(dbPath)");
        }
        return instance;
    }

    public Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }

    private void initTables() {
        String[] ddl = {
            """
            CREATE TABLE IF NOT EXISTS users (
                id          TEXT PRIMARY KEY,
                name        TEXT NOT NULL,
                avatar      TEXT,
                created_at  TEXT DEFAULT (datetime('now')),
                updated_at  TEXT DEFAULT (datetime('now'))
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS todos (
                id          TEXT PRIMARY KEY,
                title       TEXT NOT NULL,
                description TEXT,
                status      TEXT DEFAULT 'PENDING',
                priority    TEXT DEFAULT 'MEDIUM',
                assignee_id TEXT REFERENCES users(id),
                due_date    TEXT,
                start_date  TEXT,
                tags        TEXT,
                sort_order  INTEGER DEFAULT 0,
                completed   INTEGER DEFAULT 0,
                completed_at TEXT,
                created_at  TEXT DEFAULT (datetime('now')),
                updated_at  TEXT DEFAULT (datetime('now'))
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id          TEXT PRIMARY KEY,
                todo_id     TEXT REFERENCES todos(id) ON DELETE CASCADE,
                remind_at   TEXT NOT NULL,
                triggered   INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now'))
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS comments (
                id          TEXT PRIMARY KEY,
                todo_id     TEXT REFERENCES todos(id) ON DELETE CASCADE,
                user_id     TEXT REFERENCES users(id),
                content     TEXT NOT NULL,
                created_at  TEXT DEFAULT (datetime('now'))
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS activity_log (
                id          TEXT PRIMARY KEY,
                todo_id     TEXT REFERENCES todos(id),
                user_id     TEXT REFERENCES users(id),
                action      TEXT NOT NULL,
                detail      TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            )
            """
        };

        try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
            for (String sql : ddl) {
                stmt.execute(sql);
            }
            log.info("数据库表初始化完成");
        } catch (SQLException e) {
            log.error("建表失败", e);
            throw new RuntimeException("数据库初始化失败", e);
        }
    }

    public void close() {
        if (dataSource != null && !dataSource.isClosed()) {
            dataSource.close();
            log.info("数据库连接池已关闭");
        }
    }
}
