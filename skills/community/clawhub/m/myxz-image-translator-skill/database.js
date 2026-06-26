import Datastore from '@seald-io/nedb';
import path from 'node:path';

/**
 * 初始化数据库
 * @param {string} saveDir 数据库存储的绝对路径 (通常是 saveDir 的根目录)
 */
export function initDB(saveDir) {
    const dbPath = path.join(saveDir, '.translate_registry.db');
    const db = new Datastore({ 
        filename: dbPath, 
        autoload: true 
    });

    // 建立唯一索引：cacheKey 是 hash_sourceLanguage_targetLanguage
    // 这保证了同一张图翻译成不同语言时，能正确区分缓存
    db.ensureIndex({ fieldName: 'cacheKey', unique: true }, (err) => {
        if (err) console.error('数据库索引创建失败:', err.message);
    });

    return db;
}

export const dbOps = {
    /**
     * 查找单条记录
     */
    find: (db, query) => {
        return new Promise((resolve, reject) => {
            db.findOne(query, (err, doc) => {
                if (err) reject(err);
                else resolve(doc); // 如果没找到，resolve(null)
            });
        });
    },

    /**
     * 插入新记录
     */
    insert: (db, doc) => {
        return new Promise((resolve, reject) => {
            // 补充插入时间，方便后续清理
            const dataToInsert = { ...doc, createdAt: Date.now() };
            db.insert(dataToInsert, (err, newDoc) => {
                if (err) reject(err);
                else resolve(newDoc);
            });
        });
    },

    /**
     * 清理过期数据 (默认保留 7 天)
     */
    cleanup: (db) => {
        const expireTime = Date.now() - 7 * 24 * 60 * 60 * 1000;
        return new Promise((resolve, reject) => {
            // 删除创建时间早于 expireTime 的记录
            db.remove({ createdAt: { $lt: expireTime } }, { multi: true }, (err, numRemoved) => {
                if (err) reject(err);
                else {
                    if (numRemoved > 0) console.log(`已清理 ${numRemoved} 条过期缓存记录`);
                    resolve(numRemoved);
                }
            });
        });
    }
};