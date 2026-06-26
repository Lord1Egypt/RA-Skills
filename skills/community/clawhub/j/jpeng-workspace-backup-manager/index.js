/**
 * Workspace Backup Manager
 * Manages workspace backups by creating snapshots and enabling restore points
 */

const fs = require('fs');
const path = require('path');

/**
 * Create a backup snapshot
 * @param {object} options - Backup options
 * @param {string} options.workspacePath - Path to workspace
 * @param {string} options.backupDir - Directory for backups
 * @param {string} options.name - Optional backup name
 * @returns {object} Backup result
 */
function createBackup(options = {}) {
  const {
    workspacePath = '/root/.openclaw/workspace',
    backupDir = '/root/.openclaw/workspace/backups',
    name = null
  } = options;

  const result = {
    timestamp: new Date().toISOString(),
    workspace_path: workspacePath,
    backup_path: null,
    files_backed_up: 0,
    size_bytes: 0,
    status: 'pending'
  };

  try {
    // Ensure backup directory exists
    if (!fs.existsSync(backupDir)) {
      fs.mkdirSync(backupDir, { recursive: true });
    }

    // Generate backup name
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupName = name || `backup-${timestamp}`;
    const backupPath = path.join(backupDir, backupName);
    
    if (fs.existsSync(backupPath)) {
      return { success: false, error: 'Backup with this name already exists', ...result };
    }

    fs.mkdirSync(backupPath, { recursive: true });
    result.backup_path = backupPath;

    // Files to backup (key workspace files)
    const filesToBackup = [
      'MEMORY.md',
      'SOUL.md',
      'IDENTITY.md',
      'AGENTS.md',
      'USER.md',
      'HEARTBEAT.md',
      'TOOLS.md'
    ];

    // Backup directories
    const dirsToBackup = [
      'memory',
      'logs'
    ];

    // Backup files
    for (const file of filesToBackup) {
      const srcPath = path.join(workspacePath, file);
      if (fs.existsSync(srcPath)) {
        const destPath = path.join(backupPath, file);
        fs.copyFileSync(srcPath, destPath);
        result.files_backed_up++;
        result.size_bytes += fs.statSync(destPath).size;
      }
    }

    // Backup directories (only if they exist and are not too large)
    for (const dir of dirsToBackup) {
      const srcDir = path.join(workspacePath, dir);
      if (fs.existsSync(srcDir)) {
        const destDir = path.join(backupPath, dir);
        copyDir(srcDir, destDir, result);
      }
    }

    // Write backup metadata
    const metadata = {
      created_at: result.timestamp,
      name: backupName,
      files_count: result.files_backed_up,
      size_bytes: result.size_bytes
    };
    fs.writeFileSync(
      path.join(backupPath, 'backup-metadata.json'),
      JSON.stringify(metadata, null, 2)
    );

    result.status = 'completed';
    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message, ...result };
  }
}

/**
 * Copy directory recursively
 */
function copyDir(src, dest, result) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath, result);
    } else {
      fs.copyFileSync(srcPath, destPath);
      result.files_backed_up++;
      result.size_bytes += fs.statSync(destPath).size;
    }
  }
}

/**
 * List available backups
 */
function listBackups(backupDir = '/root/.openclaw/workspace/backups') {
  const result = {
    backups: [],
    total_size: 0
  };

  try {
    if (!fs.existsSync(backupDir)) {
      return { success: true, ...result };
    }

    const entries = fs.readdirSync(backupDir, { withFileTypes: true });
    
    for (const entry of entries) {
      if (entry.isDirectory()) {
        const backupPath = path.join(backupDir, entry.name);
        const metadataPath = path.join(backupPath, 'backup-metadata.json');
        
        let metadata = {};
        if (fs.existsSync(metadataPath)) {
          metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
        }

        const stats = getDirStats(backupPath);
        result.total_size += stats.size;
        
        result.backups.push({
          name: entry.name,
          path: backupPath,
          created_at: metadata.created_at || 'unknown',
          files_count: metadata.files_count || stats.files,
          size_bytes: stats.size
        });
      }
    }

    // Sort by creation date (newest first)
    result.backups.sort((a, b) => 
      new Date(b.created_at) - new Date(a.created_at)
    );

    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message, ...result };
  }
}

/**
 * Get directory statistics
 */
function getDirStats(dirPath) {
  let files = 0;
  let size = 0;

  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else {
        files++;
        size += fs.statSync(fullPath).size;
      }
    }
  }

  walk(dirPath);
  return { files, size };
}

/**
 * Restore from backup
 */
function restoreBackup(options = {}) {
  const {
    backupName,
    workspacePath = '/root/.openclaw/workspace',
    backupDir = '/root/.openclaw/workspace/backups'
  } = options;

  const result = {
    timestamp: new Date().toISOString(),
    backup_name: backupName,
    files_restored: 0,
    status: 'pending'
  };

  try {
    const backupPath = path.join(backupDir, backupName);
    
    if (!fs.existsSync(backupPath)) {
      return { success: false, error: 'Backup not found', ...result };
    }

    // Restore files
    const entries = fs.readdirSync(backupPath, { withFileTypes: true });
    
    for (const entry of entries) {
      if (entry.name === 'backup-metadata.json') continue;
      
      const srcPath = path.join(backupPath, entry.name);
      const destPath = path.join(workspacePath, entry.name);
      
      if (entry.isDirectory()) {
        copyDir(srcPath, destPath, result);
      } else {
        fs.copyFileSync(srcPath, destPath);
        result.files_restored++;
      }
    }

    result.status = 'completed';
    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message, ...result };
  }
}

/**
 * Delete old backups
 */
function cleanupBackups(options = {}) {
  const {
    backupDir = '/root/.openclaw/workspace/backups',
    keepCount = 10
  } = options;

  const result = {
    deleted: [],
    kept: []
  };

  try {
    const listResult = listBackups(backupDir);
    if (!listResult.success) {
      return listResult;
    }

    const backups = listResult.backups;
    
    // Keep the most recent backups
    const toKeep = backups.slice(0, keepCount);
    const toDelete = backups.slice(keepCount);

    result.kept = toKeep.map(b => b.name);

    for (const backup of toDelete) {
      fs.rmSync(backup.path, { recursive: true });
      result.deleted.push(backup.name);
    }

    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message, ...result };
  }
}

/**
 * Format backup list
 */
function formatList(result) {
  if (!result.success) {
    return `❌ Failed to list backups: ${result.error}`;
  }

  if (result.backups.length === 0) {
    return 'No backups found.';
  }

  let output = `📦 **Available Backups** (${result.backups.length})\n\n`;
  
  for (const backup of result.backups) {
    const sizeKB = (backup.size_bytes / 1024).toFixed(1);
    output += `- **${backup.name}**\n`;
    output += `  Created: ${backup.created_at}\n`;
    output += `  Files: ${backup.files_count} | Size: ${sizeKB} KB\n\n`;
  }

  const totalMB = (result.total_size / (1024 * 1024)).toFixed(2);
  output += `Total size: ${totalMB} MB`;

  return output;
}

/**
 * Main entry point
 */
async function main() {
  console.log('Workspace Backup Manager\n');
  
  // List existing backups
  const list = listBackups();
  console.log(formatList(list));
  
  return list;
}

module.exports = {
  createBackup,
  listBackups,
  restoreBackup,
  cleanupBackups,
  formatList,
  main
};
