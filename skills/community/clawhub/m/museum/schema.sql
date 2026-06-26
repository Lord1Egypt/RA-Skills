-- Museum Database Schema
-- Compatible with MySQL 5.7+

CREATE DATABASE IF NOT EXISTS museumcheck 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE museumcheck;

CREATE TABLE IF NOT EXISTS museums (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    location VARCHAR(100),
    type VARCHAR(100),
    visitors VARCHAR(50),
    is_free VARCHAR(10),
    precious_artifacts VARCHAR(50),
    total_artifacts VARCHAR(50),
    exhibitions VARCHAR(50),
    introduction TEXT,
    top3_artifacts JSON,
    building_photo VARCHAR(500),
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    data_sources TEXT,
    INDEX idx_location (location),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
