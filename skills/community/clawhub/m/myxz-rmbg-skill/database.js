import Datastore from '@seald-io/nedb';
import path from 'path';

export function initDB(saveDir) {
    const db = new Datastore({ 
        filename: path.join(saveDir, '.rmbg_history.db'), 
        autoload: true 
    });
    db.ensureIndex({ fieldName: 'hash', unique: true });
    return db;
}

// 封装 Promise 操作
export const dbOps = {
    find: (db, query) => new Promise((res) => db.findOne(query, (err, doc) => res(doc))),
    insert: (db, doc) => new Promise((res) => db.insert(doc, (err, newDoc) => res(newDoc))),
    update: (db, query, update) => new Promise((res) => db.update(query, { $set: update }, {}, () => res())),
    // 清理 2 天前的数据
    cleanup: (db) => {
        const twoDaysAgo = Date.now() - 2 * 24 * 60 * 60 * 1000;
        return new Promise((res) => db.remove({ createdAt: { $lt: twoDaysAgo } }, { multi: true }, () => res()));
    }
};