import fs from "fs";
import path from "path";
const dbPath = path.join(process.env.HOME || "~", "/openclaw-skill-data/", "memo-knowledge.json");
function loadDB() {
    if (!fs.existsSync(dbPath)) {
        // 如果文件不存在，创建文件
        const dir = path.dirname(dbPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        const emptyDB = { memos: [] };
        fs.writeFileSync(dbPath, JSON.stringify(emptyDB, null, 2), "utf-8");
        console.log(`已创建数据库文件: ${dbPath}`);
        return emptyDB;
    }
    try {
        const content = fs.readFileSync(dbPath, "utf-8");
        return JSON.parse(content);
    }
    catch (error) {
        console.error(`读取数据库文件失败: ${error.message}`);
        console.log("返回空数据库结构");
        return { memos: [] };
    }
}
function saveDB(db) {
    try {
        // 确保目录存在
        const dir = path.dirname(dbPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(dbPath, JSON.stringify(db, null, 2), "utf-8");
    }
    catch (error) {
        console.error(`保存数据库文件失败: ${error.message}`);
        throw error;
    }
}
const action = process.argv[2];
const arg1 = process.argv[3];
const db = loadDB();
if (action === "add_memo") {
    db.memos.push({
        content: arg1,
        time: new Date().toISOString()
    });
    saveDB(db);
    console.log("备忘已记录");
}
if (action === "list_memo") {
    if (db.memos.length === 0) {
        console.log("暂无备忘");
        process.exit();
    }
    db.memos.forEach((m, i) => {
        console.log(`${i + 1}. ${m.content}`);
    });
}
if (action === "delete_memo") {
    const index = parseInt(arg1) - 1;
    if (db.memos[index]) {
        db.memos.splice(index, 1);
        saveDB(db);
        console.log("备忘已删除");
    }
    else {
        console.log("不存在该备忘");
    }
}
//# sourceMappingURL=index.js.map