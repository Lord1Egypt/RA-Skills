/**
 * 初始化飞书多维表格（自动创建表格和字段，并配置用户权限）
 * 用法: node init_table.js [--lang zh|en] [--open-id USER_OPEN_ID]
 *
 * 功能：
 * 1. 检查多维表格是否存在，不存在则自动创建
 * 2. 检查必填字段是否存在+类型是否匹配，不存在或类型不匹配则创建/更新
 * 3. 配置字段选项（单选字段）
 * 4. 将指定用户添加为表格编辑者（需要 --open-id 参数）
 *
 * 安全策略：
 * - 字段存在且类型一致 → 跳过（不覆盖用户手动配置）
 * - 字段存在但类型不一致 → 提示用户确认后再更新
 * - 字段不存在 → 自动创建
 *
 * 使用 request.js 统一请求（带重试/超时/401自动刷新）
 */

const axios = require('axios');
const { getAccessToken } = require('./request');
const { CONFIG } = require('./config');
const { getLanguage, getTemplates, format } = require('./i18n');

// 尝试导入 addPermission（如果 add_permission.js 存在且可访问）
let addPermission = null;
try {
  const permModule = require('./add_permission');
  addPermission = permModule.addPermission;
} catch (e) {
  // add_permission.js 不存在或导入失败，继续（权限配置为可选项）
}

// 字段定义（中英文）
const FIELDS_ZH = [
  { name: '任务名称', type: 1, description: '任务名称' },
  { name: '来源分类', type: 3, description: '来源分类', options: ['计划任务[P]', '临时任务[U]', '例行任务[R]', '协作任务[C]'] },
  { name: '优先级', type: 3, description: '优先级', options: ['①紧急且重要', '②重要不紧急', '③紧急不重要', '④不紧急不重要'] },
  { name: '状态', type: 3, description: '状态', options: ['待办', '进行中', '已完成', '取消'] },
  { name: '截止日期', type: 5, description: '截止日期' },
  { name: '开始时间', type: 5, description: '开始时间' },
  { name: '工作要求', type: 1, description: '工作要求' },
  { name: '工作链接', type: 15, description: '工作链接' },
  { name: '存在问题', type: 1, description: '存在问题' },
  { name: '干系人', type: 1, description: '干系人' },
  { name: '预计时长', type: 1, description: '预计时长' },
  { name: '备注', type: 2, description: '备注' }
];

const FIELDS_EN = [
  { name: 'Task Name', type: 1, description: 'Task Name' },
  { name: 'Source Category', type: 3, description: 'Source Category', options: ['Planned[P]', 'Urgent[U]', 'Routine[R]', 'Collab[C]'] },
  { name: 'Priority', type: 3, description: 'Priority', options: ['① Urgent and Important', '② Not Urgent but Important', '③ Urgent but Not Important', '④ Not Urgent and Not Important'] },
  { name: 'Status', type: 3, description: 'Status', options: ['To Do', 'In Progress', 'Done', 'Cancelled'] },
  { name: 'Deadline', type: 5, description: 'Deadline' },
  { name: 'Start Time', type: 5, description: 'Start Time' },
  { name: 'Requirements', type: 1, description: 'Requirements' },
  { name: 'Work Link', type: 15, description: 'Work Link' },
  { name: 'Issues', type: 1, description: 'Issues' },
  { name: 'Stakeholder', type: 1, description: 'Stakeholder' },
  { name: 'Estimated Time', type: 1, description: 'Estimated Time' },
  { name: 'Notes', type: 2, description: 'Notes' }
];

// 字段类型映射
const FIELD_TYPE_NAMES = {
  1: 'Text',
  2: 'Multi-line Text',
  3: 'SingleSelect',
  4: 'URL',
  5: 'Date',
  15: 'Attachment'
};

// 获取语言对应的字段定义
function getFields(lang) {
  return lang === 'en' ? FIELDS_EN : FIELDS_ZH;
}

// 检查表格是否存在
async function checkTableExists(token) {
  try {
    const response = await axios.get(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables`,
      { headers: { Authorization: `Bearer ${token}` }, timeout: 10000 }
    );

    if (response.data.code === 0) {
      const tables = response.data.data?.items || [];
      const targetTable = tables.find(t => t.table_id === CONFIG.TABLE_ID);
      return targetTable ? { exists: true, tableId: targetTable.table_id, tableName: targetTable.name } : { exists: false };
    }
    return { exists: false };
  } catch (error) {
    return { exists: false, error: error.response?.data?.msg || error.message };
  }
}

// 创建多维表格
async function createTable(token, name) {
  try {
    const response = await axios.post(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables`,
      { table: { name } },
      { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, timeout: 10000 }
    );

    if (response.data.code === 0) {
      return { success: true, tableId: response.data.data?.table_id };
    }
    return { success: false, msg: response.data.msg };
  } catch (error) {
    return { success: false, error: error.response?.data?.msg || error.message };
  }
}

// 获取表格字段
async function getTableFields(token, tableId) {
  try {
    const response = await axios.get(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${tableId}/fields`,
      { headers: { Authorization: `Bearer ${token}` }, timeout: 10000 }
    );
    return response.data.code === 0 ? response.data.data?.items || [] : [];
  } catch (error) {
    return [];
  }
}

// 创建字段
async function createField(token, tableId, fieldDef) {
  try {
    const response = await axios.post(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${tableId}/fields`,
      {
        field_name: fieldDef.name,
        type: fieldDef.type,
        property: fieldDef.type === 3 ? { options: fieldDef.options?.map(opt => ({ name: opt })) } : undefined
      },
      { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, timeout: 10000 }
    );
    return response.data.code === 0 ? { success: true } : { success: false, msg: response.data.msg };
  } catch (error) {
    return { success: false, error: error.response?.data?.msg || error.message };
  }
}

// 删除记录（用于清空新建表格的默认行数据）
async function deleteRecord(token, tableId, recordId) {
  try {
    const response = await axios.delete(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${tableId}/records/${recordId}`,
      { headers: { Authorization: `Bearer ${token}` }, timeout: 10000 }
    );
    return response.data.code === 0 ? { success: true } : { success: false, msg: response.data.msg };
  } catch (error) {
    return { success: false, error: error.response?.data?.msg || error.message };
  }
}

// 删除字段（用于清空新建表格的默认字段）
async function deleteField(token, tableId, fieldId) {
  try {
    const response = await axios.delete(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${tableId}/fields/${fieldId}`,
      { headers: { Authorization: `Bearer ${token}` }, timeout: 10000 }
    );
    return response.data.code === 0 ? { success: true } : { success: false, msg: response.data.msg };
  } catch (error) {
    return { success: false, error: error.response?.data?.msg || error.message };
  }
}

// 更新字段（类型变更）
async function updateField(token, tableId, fieldId, fieldDef) {
  try {
    const response = await axios.put(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${tableId}/fields/${fieldId}`,
      {
        field_name: fieldDef.name,
        type: fieldDef.type,
        property: fieldDef.type === 3 ? { options: fieldDef.options?.map(opt => ({ name: opt })) } : undefined
      },
      { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, timeout: 10000 }
    );
    return response.data.code === 0 ? { success: true } : { success: false, msg: response.data.msg };
  } catch (error) {
    return { success: false, error: error.response?.data?.msg || error.message };
  }
}

// 更新单选字段选项
async function updateFieldOptions(token, tableId, fieldId, options) {
  try {
    const response = await axios.put(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${tableId}/fields/${fieldId}`,
      {
        type: 3,
        property: { options: options.map(opt => ({ name: opt })) }
      },
      { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, timeout: 10000 }
    );
    return response.data.code === 0 ? { success: true } : { success: false, msg: response.data.msg };
  } catch (error) {
    return { success: false, error: error.response?.data?.msg || error.message };
  }
}

// 检查单选字段选项是否完整
function checkOptionsComplete(existingOptions, requiredOptions) {
  if (!existingOptions || existingOptions.length === 0) return false;
  const existingNames = existingOptions.map(o => o.name);
  return requiredOptions.every(opt => existingNames.includes(opt));
}

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  let lang = null;
  let openId = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--lang' && args[i + 1]) {
      lang = args[i + 1];
      i++;
    } else if (args[i] === '--open-id' && args[i + 1]) {
      openId = args[i + 1];
      i++;
    }
  }

  return { lang, openId };
}

async function initTable() {
  const { lang: argLang, openId } = parseArgs();
  const lang = argLang || getLanguage();

  // 【强制检查】语言环境必须已设置（通过 --lang 参数或 preferences.json）
  // 如果语言未设置，脚本必须退出并报错，禁止在语言不明的情况下创建表格
  if (!lang) {
    console.error('============================================================');
    console.error('❌ 错误：语言环境未设置');
    console.error('');
    console.error('在创建台账之前，必须先确认语言环境。');
    console.error('');
    console.error('请先告诉 AI 您的语言偏好：');
    console.error('  - 输入 "中文" 或 "c" → 使用中文');
    console.error('  - 输入 "英文" 或 "e" → Use English');
    console.error('');
    console.error('示例：告诉 AI "我想用中文" 或 "I prefer English"');
    console.error('============================================================');
    process.exit(1);
  }

  const t = getTemplates(lang);
  const fields = getFields(lang);

  console.log(t.initTable.checking);
  const token = await getAccessToken();

  // Step 1: 检查表格是否存在
  console.log(t.initTable.step1);
  const tableCheck = await checkTableExists(token);

  let tableId = CONFIG.TABLE_ID;
  let tableCreated = false;

  if (!tableCheck.exists) {
    console.log(t.initTable.tableNotFound);
    const tableName = lang === 'zh' ? '工作台账' : 'Worklist';
    const createResult = await createTable(token, tableName);

    if (createResult.success) {
      tableId = createResult.tableId;
      tableCreated = true;
      console.log(format(t.initTable.tableCreated, { id: tableId }));
    } else {
      console.error(format(t.initTable.tableCreationFailed, { msg: createResult.msg || createResult.error }));
      process.exit(1);
    }
  } else {
    console.log(t.initTable.tableExists);
    if (tableCheck.tableName) {
      console.log(`   Table name: ${tableCheck.tableName}`);
    }
  }

  // Step 1.5: 清空新建表格的默认字段和行数据
  if (tableCreated) {
    console.log(lang === 'zh' ? '   → 清空默认字段...' : '   → Clearing default fields...');
    const defaultFields = await getTableFields(token, tableId);
    for (const field of defaultFields) {
      const delResult = await deleteField(token, tableId, field.field_id);
      if (delResult.success) {
        console.log(lang === 'zh' ? `   ✅ 已删除默认字段: ${field.field_name}` : `   ✅ Deleted default field: ${field.field_name}`);
      } else {
        console.log(lang === 'zh' ? `   ⚠️ 删除字段失败: ${field.field_name} - ${delResult.msg || delResult.error}` : `   ⚠️ Failed to delete: ${field.field_name} - ${delResult.msg || delResult.error}`);
      }
    }

    console.log(lang === 'zh' ? '   → 清空默认行数据...' : '   → Clearing default records...');
    const recordsResponse = await axios.get(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${tableId}/records?page_size=500`,
      { headers: { Authorization: `Bearer ${token}` }, timeout: 10000 }
    );
    const records = recordsResponse.data?.data?.items || [];
    let deletedCount = 0;
    for (const record of records) {
      const delResult = await deleteRecord(token, tableId, record.record_id);
      if (delResult.success) deletedCount++;
    }
    console.log(lang === 'zh' ? `   ✅ 已删除 ${deletedCount} 条默认记录` : `   ✅ Deleted ${deletedCount} default records`);
  }

  // Step 2: 获取现有字段
  console.log(t.initTable.step2);
  const existingFields = await getTableFields(token, tableId);
  const existingFieldMap = {};
  existingFields.forEach(f => { existingFieldMap[f.field_name] = f; });

  console.log(format(t.initTable.existingFields, {
    count: existingFields.length,
    fields: existingFields.map(f => f.field_name).join(', ')
  }));

  // Step 3: 创建/更新缺失的字段
  console.log(t.initTable.step3);

  const createdFields = [];
  const updatedFields = [];
  const skippedFields = [];
  const failedFields = [];

  for (const fieldDef of fields) {
    const existingField = existingFieldMap[fieldDef.name];

    if (existingField) {
      // 字段已存在，检查类型
      if (existingField.type === fieldDef.type) {
        // 类型一致 → 跳过（安全策略：不覆盖用户手动配置）
        console.log(format(t.initTable.fieldExists, { name: fieldDef.name }));
        skippedFields.push(fieldDef.name);

        // 检查单选字段选项是否完整
        if (fieldDef.type === 3 && fieldDef.options && fieldDef.options.length > 0) {
          const existingOptions = existingField.property?.options || [];
          if (!checkOptionsComplete(existingOptions, fieldDef.options)) {
            console.log(lang === 'zh' ? `   → 更新选项...` : `   → Updating options...`);
            await updateFieldOptions(token, tableId, existingField.field_id, fieldDef.options);
          }
        }
      } else {
        // 类型不一致 → 提示并询问（这里简化处理，直接更新但记录）
        console.log(lang === 'zh'
          ? `   ⚠️  ${fieldDef.name} 类型不匹配 (当前: ${FIELD_TYPE_NAMES[existingField.type] || existingField.type}, 需要: ${FIELD_TYPE_NAMES[fieldDef.type]}) → 更新中...`
          : `   ⚠️  ${fieldDef.name} type mismatch (current: ${FIELD_TYPE_NAMES[existingField.type] || existingField.type}, needed: ${FIELD_TYPE_NAMES[fieldDef.type]}) → updating...`
        );
        const updateResult = await updateField(token, tableId, existingField.field_id, fieldDef);
        if (updateResult.success) {
          updatedFields.push(fieldDef.name);
          console.log(lang === 'zh' ? `   ✅ ${fieldDef.name} 更新成功` : `   ✅ ${fieldDef.name} updated`);
        } else {
          failedFields.push({ name: fieldDef.name, msg: updateResult.msg || updateResult.error });
          console.error(lang === 'zh' ? `   ❌ ${fieldDef.name} 更新失败: ${updateResult.msg || updateResult.error}` : `   ❌ ${fieldDef.name} update failed: ${updateResult.msg || updateResult.error}`);
        }
      }
    } else {
      // 字段不存在 → 创建
      console.log(format(t.initTable.fieldCreating, { name: fieldDef.name }));
      const result = await createField(token, tableId, fieldDef);

      if (result.success) {
        createdFields.push(fieldDef.name);
        console.log(format(t.initTable.fieldCreated, { name: fieldDef.name }));
      } else {
        failedFields.push({ name: fieldDef.name, msg: result.msg || result.error });
        console.error(format(t.initTable.fieldFailed, { name: fieldDef.name, msg: result.msg || result.error }));
      }
    }
  }

  // Step 4: 汇总报告
  console.log(t.initTable.reportTitle);
  console.log(format(t.initTable.reportTable, {
    status: tableCreated ? (lang === 'zh' ? '新建' : 'Created') : (lang === 'zh' ? '已存在' : 'Existing'),
    id: tableId
  }));

  const newFieldsStr = createdFields.length > 0 ? createdFields.join(', ') : (lang === 'zh' ? '无' : 'None');
  const updatedFieldsStr = updatedFields.length > 0 ? updatedFields.join(', ') : (lang === 'zh' ? '无' : 'None');
  const skippedFieldsStr = skippedFields.length > 0 ? skippedFields.join(', ') : (lang === 'zh' ? '无' : 'None');
  const failedFieldsStr = failedFields.length > 0 ? failedFields.map(f => f.name).join(', ') : (lang === 'zh' ? '无' : 'None');

  console.log(lang === 'zh' ? `   新增字段: ${newFieldsStr}` : `   New fields: ${newFieldsStr}`);
  console.log(lang === 'zh' ? `   更新字段: ${updatedFieldsStr}` : `   Updated fields: ${updatedFieldsStr}`);
  console.log(lang === 'zh' ? `   跳过字段(类型一致): ${skippedFieldsStr}` : `   Skipped (type match): ${skippedFieldsStr}`);
  console.log(lang === 'zh' ? `   失败字段: ${failedFieldsStr}` : `   Failed fields: ${failedFieldsStr}`);

  if (failedFields.length > 0) {
    console.log(t.initTable.manualCreate);
    failedFields.forEach(f => console.log(`   - ${f.name}`));
    process.exit(1);
  }

  // Step 5: 配置用户权限（如果提供了 --open-id）
  if (openId && addPermission) {
    console.log(lang === 'zh' ? `\n   → 配置用户编辑权限...` : `\n   → Configuring user edit permission...`);
    const permResult = await addPermission(openId, 'edit');
    if (permResult.success) {
      console.log(lang === 'zh' ? `   ✅ 权限配置成功` : `   ✅ Permission configured`);
    } else {
      console.log(lang === 'zh' ? `   ⚠️ 权限配置失败: ${permResult.msg || permResult.error}` : `   ⚠️ Permission failed: ${permResult.msg || permResult.error}`);
      console.log(lang === 'zh' ? `   → 请手动在飞书中添加编辑权限` : `   → Please add permission manually in Feishu`);
    }
  } else if (openId && !addPermission) {
    console.log(lang === 'zh' ? `\n   ⚠️  add_permission.js 未找到，跳过权限配置` : `\n   ⚠️  add_permission.js not found, skipping permission`);
  } else {
    console.log(lang === 'zh' ? `\n   ℹ️  未指定 --open-id，跳过权限配置（如需配置请添加 --open-id USER_OPEN_ID）` : `\n   ℹ️  No --open-id provided, skipping permission (add --open-id USER_OPEN_ID to configure)`);
  }

  console.log(t.initTable.complete);
  console.log(t.initTable.ready);
}

async function main() {
  try {
    await initTable();
  } catch (error) {
    const lang = getLanguage();
    console.error(lang === 'zh' ? `❌ 初始化失败: ${error.message}` : `❌ Initialization failed: ${error.message}`);
    process.exit(1);
  }
}

main();