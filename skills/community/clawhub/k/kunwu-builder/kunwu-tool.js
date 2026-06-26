#!/usr/bin/env node

/**
 * Kunwu Builder HTTP API 工具
 * 控制坤吾工业仿真软件
 */

import http from 'http';

// 支持通过环境变量配置 API 地址（默认本地，可通过 KUNWU_API_URL 覆盖）
const BASE_URL = process.env.KUNWU_API_URL || 'http://100.85.119.45:16888';
const API_HOST = new URL(BASE_URL).hostname;
const API_PORT = parseInt(new URL(BASE_URL).port);

/**
 * 延迟函数
 * @param {number} ms - 毫秒数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 调用 Kunwu Builder API（带重试机制）
 * @param {string} endpoint - API 端点
 * @param {object} data - 请求数据
 * @param {number} retries - 重试次数（默认 3 次）
 * @returns {Promise<object>} API 响应
 */
async function callAPI(endpoint, data = {}, retries = 3) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      return await callAPIInternal(endpoint, data);
    } catch (error) {
      if (attempt === retries) throw error;
      console.log(`⚠️ API 调用失败 (${endpoint})，第${attempt}次重试...`);
      await sleep(1000 * attempt); // 指数退避
    }
  }
}

/**
 * 内部 API 调用（无重试）
 */
async function callAPIInternal(endpoint, data = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, BASE_URL);
    const body = JSON.stringify(data);
    
    const options = {
      hostname: API_HOST,
      port: API_PORT,
      path: endpoint,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = http.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      res.on('end', () => {
        try {
          const result = JSON.parse(responseData);
          // 200=成功，202=异步任务已受理（也是成功）
          if (result.code === 200 || result.code === 202) {
            resolve(result);
          } else {
            reject(new Error(`API Error ${result.code}: ${result.msg}`));
          }
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error(`Connection error: ${e.message}. Is SpeedBot Builder running on port 16888?`));
    });

    req.write(body);
    req.end();
  });
}

// ============ 模型管理 ============

/**
 * 创建模型
 */
async function createModel(params) {
  return await callAPI('/model/create', {
    id: params.id,
    rename: params.rename,
    position: params.position || [0, 0, 0],
    eulerAngle: params.eulerAngle || [0, 0, 0],
    parameterizationCfg: params.parameterizationCfg,
    color: params.color,
    checkFromCloud: params.checkFromCloud || false,
  });
}

/**
 * 设置模型姿态
 */
async function setModelPose(params) {
  return await callAPI('/model/set_pose', {
    id: params.id,
    useModeId: params.useModeId,
    useLocal: params.useLocal,
    rename: params.rename,
    position: params.position,
    eulerAngle: params.eulerAngle,
    parameterizationCfg: params.parameterizationCfg,
  });
}

/**
 * 设置模型渲染颜色
 */
async function setModelRender(params) {
  return await callAPI('/model/set_render', {
    id: params.id,
    useModeId: params.useModeId,
    color: params.color,
    tempColor: params.tempColor,
  });
}

/**
 * 导出模型
 */
async function exportModel(params) {
  return await callAPI('/model/export', {
    id: params.id,
    useModeId: params.useModeId,
    type: params.type || 0, // 0:stl, 1:obj
    path: params.path,
  });
}

/**
 * 获取模型信息
 */
async function getModelInfo(params) {
  return await callAPI('/GetModelInfo', {
    id: params.id,
    useModeId: params.useModeId,
    useLocal: params.useLocal,
  });
}

/**
 * 获取所有模型信息
 */
async function getAllModelInfo() {
  return await callAPI('/GetAllModelInfo', {});
}

// ============ 机器人控制 ============

/**
 * 获取机器人位姿
 */
async function getRobotPose(params) {
  return await callAPI('/GetRobotLink', {
    id: params.id,
  });
}

/**
 * 设置机器人位姿
 */
async function setRobotPose(params) {
  return await callAPI('/SetRobotLink', {
    id: params.id,
    isJointPose: params.isJointPose,
    links: params.links,
    extraLinks: params.extraLinks,
  });
}

/**
 * 获取机器人轨迹
 */
async function getRobotTrack(params) {
  return await callAPI('/GetRobotTrackInfo', {
    id: params.id,
  });
}

/**
 * 机器人逆解
 */
async function robotSolveIK(params) {
  return await callAPI('/RobotSolveIK', {
    id: params.id,
    pos: params.pos,
    angle: params.angle,
  });
}

/**
 * 设置机器人位姿
 * isJointPose: true=关节坐标，false=直角坐标
 */
async function getRobotExtraLink(params) {
  return await callAPI('/GetRobotExtraLink', {
    id: params.id,
  });
}

/**
 * 获取地轨信息
 */
async function getGroundTrackInfo(params) {
  return await callAPI('/GetGroundTrackInfo', {
    id: params.id,
  });
}

/**
 * 查询机器人 ID（需先选中机器人）
 */
async function queryRobotId() {
  return await callAPI('/query/robot_id', {});
}

/**
 * 查询机器人位姿（流程图用）
 * poseType: 0=直角坐标，1=关节坐标
 */
async function queryRobotPos(params) {
  return await callAPI('/query/robot_pos', {
    poseType: params.poseType || 1,
  });
}

// ============ 物流设备 ============

/**
 * 控制工业设备（辊床、传送带等）
 * type: 0=辊床，1=下层辊床，2=上下横移，3=左右移动，4=传送带，5=下层传送带，6=转台，7=曲面传送带
 * command: 0=停止，1=正向运动，2=反向运动，3=自定义运动
 */
async function controlIndustrialEquipment(params) {
  return await callAPI('/motion/IndustrialEquipment', {
    id: params.id,
    type: params.type || 0,
    command: params.command || 0,
    data: params.data || {},
  });
}

/**
 * 控制自定义设备
 */
async function controlCustomEquipment(params) {
  return await callAPI('/motion/CustomEquipmentCommand', {
    id: params.id,
    data: params.data, // [{name, command}, ...]
  });
}

/**
 * 查询自定义设备状态
 */
async function queryCustomEquipment(params) {
  return await callAPI('/motion/CustomEquipmentQuery', {
    id: params.id,
    data: params.data, // [{name}, ...]
  });
}

/**
 * 到位信号
 */
async function sendRollbedSignal(params) {
  return await callAPI('/motion/rollbed', {
    id: params.id,
    type: params.type || 0,
    command: params.command || 0,
  });
}

/**
 * 连续运动点（新增）
 */
async function consecutiveWalkPoints(params) {
  return await callAPI('/motion/ConsecutiveWalkPoints', {
    Iditem: params.Iditem, // [{id, speed, jointstateArry: [{joint_state: [...]}]}, ...]
  });
}

// ============ 相机设备 ============

/**
 * 相机拍照
 */
async function cameraCapture(params) {
  return await callAPI('/sbt/sensor', {
    id: params.id,
    type: params.type || 1,
  });
}

/**
 * 查询相机列表
 */
async function queryCameraList() {
  return await callAPI('/sensor/queryCameralist', {});
}

// ============ 传感器与物流 ============

/**
 * 查询传感器状态（通用）
 */
async function getSensorStatus(params) {
  return await callAPI('/GetSensorStatus', {
    id: params.id,
  });
}

/**
 * 查询物流传感器状态
 */
async function queryLogisticSensor(params) {
  return await callAPI('/logistic/sensor', {
    id: params.id,
  });
}

/**
 * 查询零件到位状态
 * line_type: 0=托盘线，1=大件线，2=皮带线
 */
async function queryPartArrival(params) {
  return await callAPI('/logistic/steel', {
    line_type: params.line_type,
    line_id: params.line_id,
  });
}

/**
 * 下发编码器值
 */
async function setEncoderValue(params) {
  return await callAPI('/logistic/encoder', {
    id: params.id,
    value: params.value,
  });
}

/**
 * 获取传送带运动距离
 */
async function getConveyorDistance(params) {
  return await callAPI('/GetConveyorMoveDistance', {
    id: params.id,
  });
}

/**
 * 获取传送带运动距离
 */
async function resetScene() {
  return await callAPI('/ResetScene', {});
}

/**
 * 切换模式
 */
async function changeMode(params) {
  return await callAPI('/ChangeMode', {
    id: params.id, // 0:场景构建 1:行为信号 2:机器人 3:数字孪生
  });
}

/**
 * 导入 CAD 图纸
 */
async function importCAD(params) {
  return await callAPI('/import/cad_2d', {
    path: params.path,
    showProgress: params.showProgress || false,
    waitForCompletion: params.waitForCompletion || false,
    parentCADName: params.parentCADName,
  });
}

/**
 * 更新碰撞
 */
async function updateCollider(params) {
  return await callAPI('/UpdateCollider', {
    id: params.id,
  });
}

/**
 * 创建点位
 */
async function createPoints(params) {
  return await callAPI('/CreatePoints', {
    points: params.points, // [[x1,y1,z1], [x2,y2,z2], ...]
  });
}

/**
 * 场景提示
 */
async function sceneTipsShow(params) {
  return await callAPI('/SceneTipsShow', {
    id: params.id,
    Isshow: params.Isshow,
    content: params.content,
    position: params.position,
  });
}

/**
 * 获取场景 JSON - 2026-03-14 更新：软件修复后直接返回对象
 * @returns {Promise<object>} 场景数据对象（已解析）
 */
async function getSceneJson() {
  const result = await callAPI('/scene/get_scene_json', {});
  // 软件修复后：直接返回对象，不需要二次解析
  // 旧版本返回字符串：result.data.sceneJson
  // 新版本返回对象：result.data.projectData
  return result.data.projectData || result.data.sceneJson;
}

/**
 * 获取场景 JSON（已解析为对象）- 别名，与 getSceneJson 相同
 * @deprecated 使用 getSceneJson() 即可
 * @returns {Promise<object>} 解析后的场景对象
 */
async function getSceneJsonParsed() {
  return await getSceneJson();
}

/**
 * 获取层级树
 */
async function getModelTree(params) {
  return await callAPI('/models/tree', {
    rootId: params.rootId || 'scene',
    useModeId: params.useModeId || true,
    includeRoot: params.includeRoot || true,
  });
}

// ============ 行为控制（新增） ============

/**
 * 添加/更新行为（2026-03-14 更新：支持从属运动）
 */
async function addBehavior(params) {
  return await callAPI('/behavior/add', {
    id: params.id,
    useModeId: params.useModeId,
    behavioralType: params.behavioralType,
    behavioralTypeName: params.behavioralTypeName,
    referenceAxis: params.referenceAxis,
    referenceAxisName: params.referenceAxisName,
    minValue: params.minValue,
    maxValue: params.maxValue,
    runSpeed: params.runSpeed,
    targetValue: params.targetValue,
    isHaveElectricalMachinery: params.isHaveElectricalMachinery,
    offset: params.offset,
    // 从属运动字段（behavioralType=3/4 时使用）
    dependentTargetId: params.dependentTargetId,
    dependentTargetUseModeId: params.dependentTargetUseModeId,
  });
}

/**
 * 获取行为配置列表（2026-03-14 新增）
 * @param {string} id - 根模型标识（模型 ID 或名称）
 * @param {boolean} useModeId - true: 按 modelId；false: 按名称
 * @param {boolean} includeRoot - 是否包含根模型本身
 * @returns {Promise<object>} 行为配置列表
 */
async function getBehaviorList(params) {
  return await callAPI('/behavior/list', {
    id: params.id,
    useModeId: params.useModeId !== undefined ? params.useModeId : true,
    includeRoot: params.includeRoot !== undefined ? params.includeRoot : true,
  });
}

/**
 * 搜索模型（2026-03-14 新增）- 推荐用于获取 modelId
 * @param {string} keyword - 关键字，匹配 modelId/modelName/hierarchyPath
 * @param {number} limit - 最大返回数量，默认 200
 * @returns {Promise<object>} 搜索结果
 */
async function searchModel(keyword, limit = 200) {
  return await callAPI('/models/search', {
    keyword: keyword || '',
    limit: limit,
  });
}

/**
 * 获取行为参数
 */
async function getBehavior(params) {
  return await callAPI('/behavior/get', {
    id: params.id,
    useModeId: params.useModeId,
  });
}

// ============ 进度与提示（新增） ============

/**
 * AI 场景进度
 */
async function showGenerateSceneProgress(params) {
  return await callAPI('/ShowGenerateSceneProgress', {
    command: params.command || 'update',
    stageName: params.stageName,
    progress: params.progress,
  });
}

/**
 * 通用进度条
 */
async function showProgress(params) {
  return await callAPI('/view/show_progress', {
    msg: params.msg,
    value: params.value,
    isDone: params.isDone,
    showCloseButton: params.showCloseButton,
    closeMask: params.closeMask,
  });
}

// ============ 批量执行（新增） ============

/**
 * 批量执行命令
 */
async function batchExecute(params) {
  return await callAPI('/batch/execute', {
    atomic: params.atomic,
    stopOnError: params.stopOnError,
    commands: params.commands, // [{url, body}, ...]
  });
}

// ============ 排产接口（新增） ============

/**
 * 排产结果回传
 */
async function schedulingReturnResult(params) {
  return await callAPI('/scheduling/return_result', {
    code: params.code,
    msg: params.msg,
    data: params.data, // int[]
  });
}

// ============ 连续运动（新增） ============

/**
 * 连续运动点
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Kunwu Builder API Tool');
    console.log('Usage: node kunwu-tool.js <endpoint> [json-data]');
    console.log('Example: node kunwu-tool.js /GetAllModelInfo');
    process.exit(0);
  }

  const endpoint = args[0];
  let data = {};
  
  if (args[1]) {
    try {
      data = JSON.parse(args[1]);
    } catch (e) {
      console.error('Invalid JSON data');
      process.exit(1);
    }
  }

  try {
    const result = await callAPI(endpoint, data);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// 导出所有函数
export {
  callAPI,
  // 系统级 API（新增）
  systemPing,
  systemVersion,
  systemCapabilities,
  // 异步任务管理（新增）
  taskQuery,
  taskCancel,
  // 项目管理（新增）
  projectSave,
  projectLoad,
  // 模型管理
  createModel,
  setModelPose,
  setModelRender,
  exportModel,
  getModelInfo,
  getAllModelInfo,
  getModelTree,
  getSceneJson,
  getSceneJsonParsed,
  searchModel,
  destroyObject,
  destroyComponent,
  setParent,
  assemble,
  // 机器人控制
  getRobotPose,
  setRobotPose,
  getRobotTrack,
  robotSolveIK,
  getRobotExtraLink,
  getGroundTrackInfo,
  queryRobotId,
  queryRobotPos,
  consecutiveWalkPoints,
  // 物流设备
  controlIndustrialEquipment,
  controlCustomEquipment,
  queryCustomEquipment,
  sendRollbedSignal,
  getConveyorDistance,
  // 相机设备
  cameraCapture,
  queryCameraList,
  // 传感器与物流
  getSensorStatus,
  queryLogisticSensor,
  queryPartArrival,
  setEncoderValue,
  // 场景管理
  resetScene,
  changeMode,
  importCAD,
  updateCollider,
  createPoints,
  sceneTipsShow,
  // 行为控制
  addBehavior,
  getBehavior,
  getBehaviorList,
  deleteBehavior,
  // 行为配置 Helper（新增）
  createRotaryJoint,
  createLinearJoint,
  createLinearJointWithDependent,
  createBoxJoint,
  waitForTask,
  waitForTasks,
  // 进度与提示
  showGenerateSceneProgress,
  showProgress,
  // 批量执行
  batchExecute,
  // 排产接口
  schedulingReturnResult,
  // 模型库管理
  getLocalModelLibrary,
  getRemoteModelLibrary,
  deleteLocalModel,
  getModelCategories,
  favoriteModel,
  getFavoriteModels,
};

// ============ 常量定义（2026-03-13 新增，2026-03-13 18:55 更新） ============

/**
 * 行为类型枚举（BehavioralType）
 */
export const BehavioralType = {
  NONE: 0,                              // 无行为
  TRANSLATION: 1,                       // 平移（直线运动）
  ROTATE: 2,                            // 旋转运动
  TRANSLATION_DEPENDENT: 3,             // 平移（联动部件）
  ROTATE_DEPENDENT: 4,                  // 旋转（联动部件）
  LOGISTICS_TRANSLATION: 5              // 物流平移
  
  // 注释掉的枚举（暂不对外）
  // TRANSLATION_RECIPROCATE: 6,        // 平移往复
  // ROTATE_RECIPROCATE: 7              // 旋转往复
};

/**
 * 参考轴枚举（ReferenceAxis）
 */
export const ReferenceAxis = {
  X_POSITIVE: 0,    // X 正方向
  X_NEGATIVE: 1,    // X 负方向
  Y_POSITIVE: 2,    // Y 正方向
  Y_NEGATIVE: 3,    // Y 负方向
  Z_POSITIVE: 4,    // Z 正方向
  Z_NEGATIVE: 5     // Z 负方向
};

/**
 * 运行状态枚举（RunState）- 供后续扩展
 */
export const RunState = {
  STOP: 0,      // 停止
  START: 1,     // 启动
  REVERSE: 2,   // 反向
  RESET: 3      // 复位
};

/**
 * 轴向别名（简化调用）
 */
export const Axis = {
  X: ReferenceAxis.X_POSITIVE,    // 0 - X 正方向（默认）
  Y: ReferenceAxis.Y_POSITIVE,    // 2 - Y 正方向（默认）
  Z: ReferenceAxis.Z_POSITIVE     // 4 - Z 正方向（默认）
};

/**
 * 行为类型别名（简化调用）
 */
export const JointType = {
  LINEAR: BehavioralType.TRANSLATION,  // 1 - 直线运动
  ROTARY: BehavioralType.ROTATE        // 2 - 旋转运动
};

/**
 * 机器人关节预设配置（使用 ReferenceAxis 枚举）
 */
export const RobotJointPresets = {
  // 基座旋转（绕 Z 正方向，±180°）
  BASE_ROTARY: { axis: ReferenceAxis.Z_POSITIVE, min: -180, max: 180, speed: 90 },
  
  // 肩关节（绕 Y 正方向，-90° 到 90°）
  SHOULDER: { axis: ReferenceAxis.Y_POSITIVE, min: -90, max: 90, speed: 60 },
  
  // 肘关节（绕 Y 正方向，-90° 到 90°）
  ELBOW: { axis: ReferenceAxis.Y_POSITIVE, min: -90, max: 90, speed: 60 },
  
  // 腕关节旋转（绕 Z 正方向，±180°）
  WRIST_ROTATE: { axis: ReferenceAxis.Z_POSITIVE, min: -180, max: 180, speed: 120 },
  
  // 腕关节弯曲（绕 Y 正方向，-90° 到 90°）
  WRIST_BEND: { axis: ReferenceAxis.Y_POSITIVE, min: -90, max: 90, speed: 90 },
  
  // 直线模组（X 正方向，±500mm）
  LINEAR_X: { axis: ReferenceAxis.X_POSITIVE, min: -500, max: 500, speed: 100 },
  
  // 直线模组（Y 正方向，±400mm）
  LINEAR_Y: { axis: ReferenceAxis.Y_POSITIVE, min: -400, max: 400, speed: 100 },
  
  // 直线模组（Z 正方向，±300mm）
  LINEAR_Z: { axis: ReferenceAxis.Z_POSITIVE, min: -300, max: 300, speed: 80 }
};

// 运行 CLI
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

// ============ 模型库管理（2026-03-13 更新） ============

/**
 * 获取本地模型库列表
 * @param {string} name - 可选，按模型名过滤
 * @param {boolean} fuzzy - true: 模糊匹配；false: 精确匹配
 */
async function getLocalModelLibrary(params = {}) {
  return await callAPI('/model/library/local', {
    name: params.name,
    fuzzy: params.fuzzy || false,
  });
}

/**
 * 获取远程（云端）模型库列表
 * @param {string} name - 模型名称关键词
 * @param {string} type - 分类名称
 * @param {string} brand - 品牌
 * @param {string} tags - 标签
 * @param {string} group_id - 群组 ID
 * @param {number} language - 0:全部，1:中文，2:英文，-1:跟随软件
 * @param {number} pageNum - 页码（最小 1）
 * @param {number} pageSize - 每页数量（最小 1）
 */
async function getRemoteModelLibrary(params = {}) {
  return await callAPI('/model/library/remote', {
    name: params.name,
    type: params.type,
    brand: params.brand,
    tags: params.tags,
    group_id: params.group_id,
    language: params.language !== undefined ? params.language : -1,
    pageNum: params.pageNum || 1,
    pageSize: params.pageSize || 12,
  });
}

/**
 * 从本地模型库删除模型
 * @param {string} modelId - 模型 ID 或名称
 */
async function deleteLocalModel(params) {
  return await callAPI('/model/library/delete', {
    modelId: params.modelId,
  });
}

/**
 * 获取模型库分类列表
 */
async function getModelCategories() {
  return await callAPI('/model/library/categories', {});
}

/**
 * 收藏模型（添加到我的收藏）
 * @param {string} modelId - 模型 ID
 */
async function favoriteModel(params) {
  return await callAPI('/model/library/favorite', {
    modelId: params.modelId,
  });
}

/**
 * 获取收藏的模型列表
 */
async function getFavoriteModels() {
  return await callAPI('/model/library/favorites', {});
}

// ============ 层级与销毁（2026-03-13 更新） ============

/**
 * 设置物体层级关系（父子关系）
 * @param {string} childId - 子物体 modelId 或名称
 * @param {string} parentId - 父物体 modelId 或名称，null/undefined 表示解除父子关系
 * @param {boolean} childUseModeId - 子物体是否使用 modelId 查找
 * @param {boolean} parentUseModeId - 父物体是否使用 modelId 查找
 * @param {boolean} worldPositionStays - 设置父级时是否保持世界坐标
 */
async function setParent(params) {
  return await callAPI('/model/set_parent', {
    childId: params.childId,
    parentId: params.parentId,
    childUseModeId: params.childUseModeId !== undefined ? params.childUseModeId : true,
    parentUseModeId: params.parentUseModeId !== undefined ? params.parentUseModeId : true,
    worldPositionStays: params.worldPositionStays !== undefined ? params.worldPositionStays : true,
  });
}

/**
 * 销毁物体（支持批量）
 * @param {string} id - 单个物体 modelId 或名称
 * @param {string[]} ids - 批量物体 modelId 或名称数组
 * @param {boolean} useModeId - 是否使用 modelId 查找
 */
async function destroyObject(params) {
  return await callAPI('/model/destroy', {
    id: params.id,
    ids: params.ids,
    useModeId: params.useModeId !== undefined ? params.useModeId : true,
  });
}

/**
 * 销毁组件
 * @param {string} id - 物体 modelId 或名称
 * @param {string} componentType - 组件类型 (BehavioralSetting, Collider 等)
 * @param {boolean} useModeId - 是否使用 modelId 查找
 */
async function destroyComponent(params) {
  return await callAPI('/model/destroy_component', {
    id: params.id,
    componentType: params.componentType,
    useModeId: params.useModeId !== undefined ? params.useModeId : true,
  });
}

// ============ 装配功能（2026-03-13 更新） ============

/**
 * 装配（将物体装配到指定位置）- 专业装配接口
 * @param {string} childId - 子模型 modelId 或名称
 * @param {string} parentId - 父模型 modelId 或名称
 * @param {boolean} childUseModeId - 子模型是否按 modelId 查找
 * @param {boolean} parentUseModeId - 父模型是否按 modelId 查找
 * @param {string} assemblePosName - 可选：指定装配位名称
 * @param {number} assemblePosIndex - 可选：指定装配位索引，-1 表示自动选择
 * @param {boolean} replaceExisting - 装配位被占用时是否替换
 */
async function assemble(params) {
  return await callAPI('/model/assemble', {
    childId: params.childId,
    parentId: params.parentId,
    childUseModeId: params.childUseModeId !== undefined ? params.childUseModeId : true,
    parentUseModeId: params.parentUseModeId !== undefined ? params.parentUseModeId : true,
    assemblePosName: params.assemblePosName,
    assemblePosIndex: params.assemblePosIndex !== undefined ? params.assemblePosIndex : -1,
    replaceExisting: params.replaceExisting !== undefined ? params.replaceExisting : true,
  });
}

// ============ 系统级 API（2026-03-13 新增） ============

/**
 * 系统健康检查
 * @returns {object} { status: "ok", serverTimeUnixMs: timestamp }
 */
async function systemPing() {
  return await callAPI('/system/ping', {});
}

/**
 * 获取系统版本信息
 * @returns {object} { appVersion, protocolVersion, unityVersion, productName, appStage }
 */
async function systemVersion() {
  return await callAPI('/system/version', {});
}

/**
 * 获取系统能力清单（返回支持的接口和功能开关）
 * @returns {object} { protocolVersion, endpoints: [], features: {} }
 */
async function systemCapabilities() {
  return await callAPI('/system/capabilities', {});
}

// ============ 异步任务管理（2026-03-13 新增） ============

/**
 * 查询异步任务状态
 * @param {string} taskId - 任务 ID
 * @returns {object} { taskId, operation, status, done, resultCode, resultData }
 */
async function taskQuery(params) {
  return await callAPI('/task/query', {
    taskId: params.taskId,
  });
}

/**
 * 取消异步任务（best-effort）
 * @param {string} taskId - 任务 ID
 * @returns {object} { taskId, status: "Cancelled", cancelled: true }
 */
async function taskCancel(params) {
  return await callAPI('/task/cancel', {
    taskId: params.taskId,
  });
}

// ============ 项目管理（2026-03-13 新增） ============

/**
 * 异步保存项目
 * @param {string} path - 项目文件路径（自动补 .kunwuproject 扩展名）
 * @returns {object} 任务受理返回 taskId，通过 taskQuery 查询结果
 */
async function projectSave(params) {
  return await callAPI('/project/save', {
    path: params.path,
  });
}

/**
 * 异步加载项目
 * @param {string} path - 项目文件路径
 * @param {boolean} savePathFlag - 是否将该路径写入当前工程路径
 * @returns {object} 任务受理返回 taskId，通过 taskQuery 查询结果
 */
async function projectLoad(params) {
  return await callAPI('/project/load', {
    path: params.path,
    savePathFlag: params.savePathFlag !== undefined ? params.savePathFlag : true,
  });
}

// ============ 行为管理补充（2026-03-13 新增） ============

/**
 * 删除行为组件
 * @param {string} id - 模型 modelId 或名称
 * @param {boolean} useModeId - 是否使用 modelId 查找
 */
async function deleteBehavior(params) {
  return await callAPI('/behavior/delete', {
    id: params.id,
    useModeId: params.useModeId !== undefined ? params.useModeId : true,
  });
}

// ============ 行为配置 Helper 函数（2026-03-13 新增） ============

/**
 * 创建旋转关节（简化调用）- 2026-03-14 更新：支持从属运动
 * @param {string} modelId - 模型 ID
 * @param {number|string} axis - 旋转轴 (ReferenceAxis 枚举值或名称)
 * @param {number} minAngle - 最小角度（度）
 * @param {number} maxAngle - 最大角度（度）
 * @param {number} speed - 速度（度/秒），默认 60
 * @param {boolean} useAxisName - 是否使用轴名称（默认 false，使用枚举值）
 * @param {string} dependentTargetId - 从属目标模型 ID（可选，用于联动部件）
 * @returns {Promise<object>} API 响应
 */
async function createRotaryJoint(modelId, axis, minAngle, maxAngle, speed = 60, useAxisName = false, dependentTargetId = null) {
  const params = {
    id: modelId,
    useModeId: true,
    behavioralType: dependentTargetId ? BehavioralType.ROTATE_DEPENDENT : BehavioralType.ROTATE,
    minValue: minAngle,
    maxValue: maxAngle,
    runSpeed: speed,
    isHaveElectricalMachinery: true
  };
  
  if (useAxisName) {
    params.referenceAxisName = axis;
  } else {
    params.referenceAxis = axis;
  }
  
  if (dependentTargetId) {
    params.dependentTargetId = dependentTargetId;
    params.dependentTargetUseModeId = true;
  }
  
  return await addBehavior(params);
}

/**
 * 创建直线关节（简化调用）- 2026-03-14 更新：支持层级路径
 * @param {string} modelId - 模型 ID 或层级路径
 * @param {number|string} axis - 运动轴 (ReferenceAxis 枚举值或名称)
 * @param {number} minPos - 最小位置（mm）
 * @param {number} maxPos - 最大位置（mm）
 * @param {number} speed - 速度（mm/秒），默认 100
 * @param {boolean} useModeId - true: 按 modelId；false: 按名称/路径（默认 true）
 * @param {string} dependentTargetId - 从属目标模型 ID 或路径（可选）
 * @param {boolean} dependentTargetUseModeId - 从属目标查找方式（默认与 useModeId 一致）
 * @returns {Promise<object>} API 响应
 */
async function createLinearJoint(modelId, axis, minPos, maxPos, speed = 100, useModeId = true, dependentTargetId = null, dependentTargetUseModeId = null) {
  const params = {
    id: modelId,
    useModeId: useModeId,
    behavioralType: dependentTargetId ? BehavioralType.TRANSLATION_DEPENDENT : BehavioralType.TRANSLATION,
    minValue: minPos,
    maxValue: maxPos,
    runSpeed: speed,
    isHaveElectricalMachinery: true
  };
  
  if (typeof axis === 'string') {
    params.referenceAxisName = axis;
  } else {
    params.referenceAxis = axis;
  }
  
  if (dependentTargetId) {
    params.dependentTargetId = dependentTargetId;
    params.dependentTargetUseModeId = dependentTargetUseModeId !== null ? dependentTargetUseModeId : useModeId;
  }
  
  return await addBehavior(params);
}

/**
 * 创建直线关节（从动臂）- 2026-03-14 新增
 * 用于创建联动部件，自动设置 behavioralType=3
 * @param {string} modelId - 从动臂模型 ID 或路径
 * @param {number|string} axis - 运动轴
 * @param {number} minPos - 最小位置（mm）
 * @param {number} maxPos - 最大位置（mm）
 * @param {number} speed - 速度（mm/秒），默认 100
 * @param {string} dependentTargetId - 主动臂模型 ID 或路径（必须）
 * @param {boolean} useModeId - true: 按 modelId；false: 按名称/路径
 * @returns {Promise<object>} API 响应
 */
async function createLinearJointWithDependent(modelId, axis, minPos, maxPos, speed = 100, dependentTargetId, useModeId = true) {
  return await createLinearJoint(modelId, axis, minPos, maxPos, speed, useModeId, dependentTargetId, useModeId);
}

/**
 * 创建参数化方形关节（简化调用）- 2026-03-14 修复：支持可变参数
 * @param {string} name - 关节名称
 * @param {number[]} position - 位置 [x, y, z]（mm，软件单位）
 * @param {number} length - 长度（mm，type: 0）
 * @param {number} width - 宽度（mm，type: 1）
 * @param {number} [height] - 高度（mm，type: 2，可选）
 * @returns {Promise<object>} API 响应
 */
async function createBoxJoint(name, position, length, width, height) {
  // 构建参数化配置（只包含有值的参数）
  const parameterizationCfg = [
    { type: 0, value: length },  // 长（mm）
    { type: 1, value: width },   // 宽（mm）
  ];
  
  // 高度是可选参数（方形模型可能只支持长宽 2 个参数）
  if (height !== undefined && height !== null) {
    parameterizationCfg.push({ type: 2, value: height });
  }
  
  // 优先使用 /model/create（检查本地仓库，避免重复下载）
  return await createModel({
    id: '方形',  // 本地模型库中的名称
    rename: name,
    position: position,
    eulerAngle: [0, 0, 0],
    parameterizationCfg: parameterizationCfg,
  });
}

/**
 * 等待异步任务完成（轮询）
 * @param {string} taskId - 任务 ID
 * @param {number} intervalMs - 轮询间隔（ms），默认 2000
 * @param {number} timeoutMs - 超时时间（ms），默认 60000
 * @returns {Promise<object>} 任务结果
 */
async function waitForTask(taskId, intervalMs = 2000, timeoutMs = 60000) {
  const startTime = Date.now();
  
  while (true) {
    const status = await taskQuery({ taskId });
    
    if (status.data.done) {
      if (status.data.resultCode === 200) {
        return status.data;
      } else {
        throw new Error(`Task failed: ${status.data.resultMsg}`);
      }
    }
    
    if (Date.now() - startTime > timeoutMs) {
      throw new Error('Task timeout');
    }
    
    await new Promise(r => setTimeout(r, intervalMs));
  }
}

/**
 * 等待多个任务完成
 * @param {string[]} taskIds - 任务 ID 数组
 * @returns {Promise<Array<object>>} 所有任务结果
 */
async function waitForTasks(taskIds) {
  return await Promise.all(taskIds.map(taskId => waitForTask(taskId)));
}

