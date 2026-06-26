/**
 * Version Manager Module
 * Handle database backups, migrations, and rollbacks
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class VersionManager {
    constructor(db, backupDir = './backups') {
        this.db = db;
        this.backupDir = backupDir;
        
        // Ensure backup directory exists
        if (!fs.existsSync(backupDir)) {
            fs.mkdirSync(backupDir, { recursive: true });
        }
    }

    /**
     * Create database backup
     */
    async createBackup(description = '', type = 'full') {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const backupName = `memory-v2-${type}-${timestamp}`;
        const backupPath = path.join(this.backupDir, `${backupName}.db`);

        // Copy database file
        const dbPath = this.db.dbPath;
        await this.copyFile(dbPath, backupPath);

        // Calculate checksum
        const checksum = await this.calculateChecksum(backupPath);
        const stats = fs.statSync(backupPath);

        // Record version
        const result = await this.db.run(
            `INSERT INTO memory_versions 
             (version_name, version_type, description, backup_path, backup_size, checksum)
             VALUES (?, ?, ?, ?, ?, ?)`,
            [backupName, type, description, backupPath, stats.size, checksum]
        );

        // Record table statistics
        await this.recordTableStats(result.id);

        return {
            success: true,
            versionId: result.id,
            backupPath,
            size: stats.size,
            checksum
        };
    }

    /**
     * Copy file (promise wrapper)
     */
    copyFile(src, dest) {
        return new Promise((resolve, reject) => {
            fs.copyFile(src, dest, (err) => {
                if (err) reject(err);
                else resolve();
            });
        });
    }

    /**
     * Calculate file checksum
     */
    calculateChecksum(filePath) {
        return new Promise((resolve, reject) => {
            const hash = crypto.createHash('sha256');
            const stream = fs.createReadStream(filePath);
            
            stream.on('data', data => hash.update(data));
            stream.on('end', () => resolve(hash.digest('hex')));
            stream.on('error', reject);
        });
    }

    /**
     * Record table statistics
     */
    async recordTableStats(versionId) {
        const tables = [
            'memory_priorities',
            'memory_learning',
            'memory_learning_milestones',
            'memory_decisions',
            'memory_evolution',
            'memory_evolution_history',
            'memory_versions',
            'memory_version_stats'
        ];

        for (const table of tables) {
            try {
                const count = await this.db.get(
                    `SELECT COUNT(*) as count FROM ${table}`
                );
                
                await this.db.run(
                    `INSERT INTO memory_version_stats (version_id, table_name, record_count)
                     VALUES (?, ?, ?)`,
                    [versionId, table, count.count]
                );
            } catch (err) {
                console.warn(`Table ${table} not found or error:`, err.message);
            }
        }
    }

    /**
     * List all versions
     */
    async listVersions() {
        const sql = `
            SELECT v.*, 
                   GROUP_CONCAT(s.table_name || ': ' || s.record_count, ', ') as table_stats
            FROM memory_versions v
            LEFT JOIN memory_version_stats s ON v.id = s.version_id
            GROUP BY v.id
            ORDER BY v.created_at DESC
        `;
        return await this.db.all(sql);
    }

    /**
     * Get active version
     */
    async getActiveVersion() {
        return await this.db.get(
            `SELECT * FROM memory_versions WHERE is_active = 1`
        );
    }

    /**
     * Activate version
     */
    async activateVersion(versionId) {
        // Deactivate current active version
        await this.db.run(
            `UPDATE memory_versions SET is_active = 0 WHERE is_active = 1`
        );

        // Activate new version
        await this.db.run(
            `UPDATE memory_versions 
             SET is_active = 1, activated_at = CURRENT_TIMESTAMP 
             WHERE id = ?`,
            [versionId]
        );

        return { success: true, versionId };
    }

    /**
     * Rollback to version
     */
    async rollbackToVersion(versionId) {
        const version = await this.db.get(
            `SELECT * FROM memory_versions WHERE id = ?`,
            [versionId]
        );

        if (!version) {
            return { success: false, error: 'Version not found' };
        }

        if (!fs.existsSync(version.backup_path)) {
            return { success: false, error: 'Backup file not found' };
        }

        // Create backup before rollback
        await this.createBackup(`Pre-rollback to v${versionId}`, 'pre-rollback');

        // Copy backup to active database
        await this.copyFile(version.backup_path, this.db.dbPath);

        // Activate version
        await this.activateVersion(versionId);

        return {
            success: true,
            rolledBackTo: version.version_name,
            timestamp: version.created_at
        };
    }

    /**
     * Delete old backups
     */
    async cleanupOldBackups(days = 30, keepLastN = 5) {
        // Get backups to delete
        const oldBackups = await this.db.all(
            `SELECT * FROM memory_versions 
             WHERE version_type = 'full' 
             AND created_at < datetime('now', '-${days} days')
             ORDER BY created_at DESC`
        );

        // Keep last N backups
        const toDelete = oldBackups.slice(keepLastN);
        let deletedCount = 0;

        for (const backup of toDelete) {
            try {
                if (fs.existsSync(backup.backup_path)) {
                    fs.unlinkSync(backup.backup_path);
                }
                await this.db.run(
                    `DELETE FROM memory_version_stats WHERE version_id = ?`,
                    [backup.id]
                );
                await this.db.run(
                    `DELETE FROM memory_versions WHERE id = ?`,
                    [backup.id]
                );
                deletedCount++;
            } catch (err) {
                console.error(`Failed to delete backup ${backup.version_name}:`, err);
            }
        }

        return { deleted: deletedCount };
    }

    /**
     * Get backup statistics
     */
    async getBackupStats() {
        const stats = await this.db.get(
            `SELECT 
                COUNT(*) as total_backups,
                SUM(backup_size) as total_size,
                AVG(backup_size) as avg_size,
                MAX(created_at) as last_backup,
                MIN(created_at) as first_backup
             FROM memory_versions
             WHERE version_type = 'full'`
        );

        return {
            totalBackups: stats.total_backups || 0,
            totalSize: stats.total_size || 0,
            avgSize: stats.avg_size || 0,
            lastBackup: stats.last_backup,
            firstBackup: stats.first_backup
        };
    }

    /**
     * Verify backup integrity
     */
    async verifyBackup(versionId) {
        const version = await this.db.get(
            `SELECT * FROM memory_versions WHERE id = ?`,
            [versionId]
        );

        if (!version) {
            return { valid: false, error: 'Version not found' };
        }

        if (!fs.existsSync(version.backup_path)) {
            return { valid: false, error: 'Backup file missing' };
        }

        const currentChecksum = await this.calculateChecksum(version.backup_path);
        
        if (currentChecksum !== version.checksum) {
            return { 
                valid: false, 
                error: 'Checksum mismatch',
                expected: version.checksum,
                actual: currentChecksum
            };
        }

        return { valid: true, checksum: currentChecksum };
    }
}

module.exports = VersionManager;