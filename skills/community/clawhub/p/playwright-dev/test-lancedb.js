const lancedb = require('@lancedb/lancedb');

async function test() {
  console.log("=== LanceDB 完整测试 ===");
  console.log("");
  
  try {
    // 创建数据库
    const uri = "C:\\Users\\Xiabi\\AppData\\Local\\Temp\\test-lancedb";
    const db = await lancedb.connect(uri);
    console.log("✅ 1. 数据库连接成功");
    
    // 创建测试表
    const data = [
      { id: 1, text: "香香测试 1", vector: Array(1024).fill(0.1) },
      { id: 2, text: "香香测试 2", vector: Array(1024).fill(0.2) }
    ];
    const table = await db.createTable("test", data);
    console.log("✅ 2. 表创建成功");
    
    // 查询测试
    const query = Array(1024).fill(0.15);
    const results = await table.search(query).limit(2).execute();
    console.log("✅ 3. 向量搜索成功");
    console.log("   结果数量:", results ? results.length : "N/A");
    
    // 显示结果
    if (results && results.length > 0) {
      console.log("✅ 4. 结果可遍历");
      for (let i = 0; i < results.length; i++) {
        console.log(`   ${i+1}. ${results[i].text}`);
      }
    }
    
    await db.close();
    console.log("");
    console.log("🎉 LanceDB 所有功能正常！");
  } catch (err) {
    console.error("❌ 错误:", err.message);
  }
}

test();
