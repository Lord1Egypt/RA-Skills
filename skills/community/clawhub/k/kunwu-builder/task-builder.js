#!/usr/bin/env node

/**
 * Task Builder for Kunwu Builder
 * 高级任务构建器 - 将业务任务自动分解为 API 调用
 */

import {
  createModel,
  setParent,
  addBehavior,
  createRotaryJoint,
  createLinearJoint,
  BehavioralType,
  ReferenceAxis,
  getAllModelInfo,
  taskQuery,
  waitForTasks
} from './kunwu-tool.js';

/**
 * 任务执行统计
 */
const executionStats = {
  totalTasks: 0,
  successfulTasks: 0,
  failedTasks: 0,
  averageDuration: 0,
  commonPatterns: [],
  optimizationSuggestions: []
};

/**
 * Task Builder 主类
 */
class TaskBuilder {
  constructor() {
    this.createdModels = [];
    this.createdBehaviors = [];
    this.taskHistory = [];
  }

  /**
   * 创建气缸工位
   */
  async createCylinderStation(params) {
    const startTime = Date.now();
    executionStats.totalTasks++;

    try {
      const defaults = {
        name: 'cylinder_station',
        position: [0, 0, 0],
        cylinder: {
          type: 'push',
          stroke: 100,
          speed: 50,
          homePosition: 0
        },
        sensor: {
          type: 'proximity',
          position: 'top'
        }
      };

      const config = { ...defaults, ...params };

      // 1. 创建气缸基座（使用 createModel + checkFromCloud=true）
      console.log(`📦 创建气缸基座：${config.name}`);
      await createModel({
        id: '方形',
        rename: `${config.name}_base`,
        position: config.position,
        checkFromCloud: true,
        parameterizationCfg: [
          { type: 0, value: 200 },
          { type: 1, value: 100 },
          { type: 2, value: 50 }
        ]
      });

      // 2. 创建气缸杆
      console.log(`📦 创建气缸杆`);
      await createModel({
        id: '方形',
        rename: `${config.name}_rod`,
        position: [
          config.position[0],
          config.position[1],
          config.position[2] + 50
        ],
        checkFromCloud: true,
        parameterizationCfg: [
          { type: 0, value: 50 },
          { type: 1, value: 50 },
          { type: 2, value: config.cylinder.stroke }
        ]
      });
      
      if (taskIds.length > 0) {
        console.log(`⏳ 等待模型创建完成 (${taskIds.length}个任务)...`);
        await waitForTasks(taskIds);
      }

      // 4. 查询 modelId
      const models = await getAllModelInfo();
      const baseModel = models.data.models.find(m => m.modelName === `${config.name}_base`);
      const rodModel = models.data.models.find(m => m.modelName === `${config.name}_rod`);

      // 5. 配置层级关系
      if (baseModel && rodModel) {
        console.log(`🔗 配置层级关系`);
        await setParent({
          childId: rodModel.modelId,
          parentId: baseModel.modelId,
          childUseModeId: true,
          parentUseModeId: true
        });

        // 6. 添加直线运动行为（气缸杆）
        console.log(`🎯 添加气缸运动行为`);
        await createLinearJoint(
          rodModel.modelId,
          ReferenceAxis.Z_POSITIVE,
          0,
          config.cylinder.stroke,
          config.cylinder.speed
        );

        this.createdBehaviors.push({
          modelId: rodModel.modelId,
          type: 'cylinder',
          config: config.cylinder
        });
      }

      const duration = Date.now() - startTime;
      executionStats.successfulTasks++;
      this._recordSuccess('createCylinderStation', duration);

      console.log(`✅ 气缸工位创建完成 (${duration}ms)`);
      return { success: true, duration, models: [baseModel, rodModel] };

    } catch (error) {
      executionStats.failedTasks++;
      this._recordFailure('createCylinderStation', error);
      await this._rollback();
      throw error;
    }
  }

  /**
   * 创建夹爪工位
   */
  async createGripperStation(params) {
    const startTime = Date.now();
    executionStats.totalTasks++;

    try {
      const defaults = {
        name: 'gripper_station',
        position: [0, 0, 0],
        gripper: {
          type: '2-jaw',
          opening: 50,
          force: 100,
          speed: 80
        }
      };

      const config = { ...defaults, ...params };

      // 1. 创建夹爪基座
      console.log(`📦 创建夹爪基座：${config.name}`);
      const baseTask = await createModel({
        id: '方形',
        rename: `${config.name}_base`,
        position: config.position,
        parameterizationCfg: [
          { type: 0, value: 150 },
          { type: 1, value: 150 },
          { type: 2, value: 100 }
        ]
      });

      // 2. 创建夹爪手指（2 个）
      console.log(`📦 创建夹爪手指`);
      const finger1Task = await createModel({
        id: '方形',
        rename: `${config.name}_finger1`,
        position: [
          config.position[0] - 25,
          config.position[1],
          config.position[2] + 100
        ],
        parameterizationCfg: [
          { type: 0, value: 30 },
          { type: 1, value: 80 },
          { type: 2, value: 40 }
        ]
      });

      const finger2Task = await createModel({
        id: '方形',
        rename: `${config.name}_finger2`,
        position: [
          config.position[0] + 25,
          config.position[1],
          config.position[2] + 100
        ],
        parameterizationCfg: [
          { type: 0, value: 30 },
          { type: 1, value: 80 },
          { type: 2, value: 40 }
        ]
      });

      // 3. 等待完成
      const taskIds = [baseTask.data?.taskId, finger1Task.data?.taskId, finger2Task.data?.taskId].filter(Boolean);
      if (taskIds.length > 0) {
        await waitForTasks(taskIds);
      }

      // 4. 查询 modelId
      const models = await getAllModelInfo();
      const baseModel = models.data.models.find(m => m.modelName === `${config.name}_base`);
      const finger1Model = models.data.models.find(m => m.modelName === `${config.name}_finger1`);
      const finger2Model = models.data.models.find(m => m.modelName === `${config.name}_finger2`);

      // 5. 配置层级关系
      if (baseModel && finger1Model && finger2Model) {
        console.log(`🔗 配置层级关系`);
        await setParent({
          childId: finger1Model.modelId,
          parentId: baseModel.modelId,
          childUseModeId: true,
          parentUseModeId: true
        });

        await setParent({
          childId: finger2Model.modelId,
          parentId: baseModel.modelId,
          childUseModeId: true,
          parentUseModeId: true
        });

        // 6. 添加夹爪开合行为（直线运动）
        console.log(`🎯 添加夹爪开合行为`);
        
        // 手指 1：X 负方向运动
        await createLinearJoint(
          finger1Model.modelId,
          ReferenceAxis.X_NEGATIVE,
          0,
          config.gripper.opening / 2,
          config.gripper.speed
        );

        // 手指 2：X 正方向运动
        await createLinearJoint(
          finger2Model.modelId,
          ReferenceAxis.X_POSITIVE,
          0,
          config.gripper.opening / 2,
          config.gripper.speed
        );

        this.createdBehaviors.push({
          modelId: finger1Model.modelId,
          type: 'gripper_finger',
          config: config.gripper
        });
        this.createdBehaviors.push({
          modelId: finger2Model.modelId,
          type: 'gripper_finger',
          config: config.gripper
        });
      }

      const duration = Date.now() - startTime;
      executionStats.successfulTasks++;
      this._recordSuccess('createGripperStation', duration);

      console.log(`✅ 夹爪工位创建完成 (${duration}ms)`);
      return { success: true, duration, models: [baseModel, finger1Model, finger2Model] };

    } catch (error) {
      executionStats.failedTasks++;
      this._recordFailure('createGripperStation', error);
      await this._rollback();
      throw error;
    }
  }

  /**
   * 创建传送带线
   */
  async createConveyorLine(params) {
    const startTime = Date.now();
    executionStats.totalTasks++;

    try {
      const defaults = {
        name: 'conveyor_line',
        position: [0, 0, 0],
        sections: [
          { length: 1000, speed: 200, direction: 'forward' }
        ]
      };

      const config = { ...defaults, ...params };

      const createdModels = [];

      // 创建每个传送带段
      let currentPosition = [...config.position];
      for (let i = 0; i < config.sections.length; i++) {
        const section = config.sections[i];
        console.log(`📦 创建传送带段 ${i + 1}/${config.sections.length}`);

        const task = await createModel({
          id: '皮带线',
          rename: `${config.name}_section${i + 1}`,
          position: currentPosition,
          parameterizationCfg: [
            { type: 0, value: section.length },
            { type: 1, value: 200 },
            { type: 2, value: 100 }
          ]
        });

        if (task.data?.taskId) {
          createdModels.push(task.data.taskId);
        }

        currentPosition[0] += section.length;
      }

      // 等待所有传送带段创建完成
      if (createdModels.length > 0) {
        await waitForTasks(createdModels);
      }

      const duration = Date.now() - startTime;
      executionStats.successfulTasks++;
      this._recordSuccess('createConveyorLine', duration);

      console.log(`✅ 传送带线创建完成 (${duration}ms, ${config.sections.length}段)`);
      return { success: true, duration, sections: config.sections.length };

    } catch (error) {
      executionStats.failedTasks++;
      this._recordFailure('createConveyorLine', error);
      await this._rollback();
      throw error;
    }
  }

  /**
   * 创建机器人工作站（机器人已有行为配置，只需创建周边设备）
   */
  async createRobotStation(params) {
    const startTime = Date.now();
    executionStats.totalTasks++;

    try {
      const defaults = {
        name: 'robot_station',
        robot: {
          model: 'IRB6700',
          position: [0, 0, 0]
        },
        infeed: {
          type: 'conveyor',
          position: [-500, 0, 0]
        },
        outfeed: {
          type: 'conveyor',
          position: [500, 0, 0]
        }
      };

      const config = { ...defaults, ...params };

      console.log(`🤖 创建机器人工作站：${config.name}`);

      // 1. 创建进料传送带
      console.log(`📦 创建进料传送带`);
      await this.createConveyorLine({
        name: `${config.name}_infeed`,
        position: config.infeed.position,
        sections: [{ length: 1000, speed: 200 }]
      });

      // 2. 创建出料传送带
      console.log(`📦 创建出料传送带`);
      await this.createConveyorLine({
        name: `${config.name}_outfeed`,
        position: config.outfeed.position,
        sections: [{ length: 1000, speed: 200 }]
      });

      // 注意：机器人模型从云端下载时已自带行为配置，不需要额外添加

      const duration = Date.now() - startTime;
      executionStats.successfulTasks++;
      this._recordSuccess('createRobotStation', duration);

      console.log(`✅ 机器人工作站创建完成 (${duration}ms)`);
      return { success: true, duration };

    } catch (error) {
      executionStats.failedTasks++;
      this._recordFailure('createRobotStation', error);
      await this._rollback();
      throw error;
    }
  }

  /**
   * 记录成功执行
   */
  _recordSuccess(taskName, duration) {
    this.taskHistory.push({
      task: taskName,
      success: true,
      duration,
      timestamp: Date.now()
    });

    // 更新平均耗时
    const recentTasks = this.taskHistory.slice(-10);
    executionStats.averageDuration = recentTasks.reduce((sum, t) => sum + t.duration, 0) / recentTasks.length;

    // 记录常见模式
    const pattern = executionStats.commonPatterns.find(p => p.task === taskName);
    if (pattern) {
      pattern.count++;
    } else {
      executionStats.commonPatterns.push({ task: taskName, count: 1 });
    }
  }

  /**
   * 记录失败执行
   */
  _recordFailure(taskName, error) {
    this.taskHistory.push({
      task: taskName,
      success: false,
      error: error.message,
      timestamp: Date.now()
    });

    // 记录优化建议
    executionStats.optimizationSuggestions.push({
      task: taskName,
      issue: error.message,
      suggestion: `检查参数配置或 API 可用性`
    });
  }

  /**
   * 回滚操作（失败时清理）
   */
  async _rollback() {
    console.log(`🔄 执行回滚操作...`);
    // TODO: 实现回滚逻辑
    this.createdModels = [];
    this.createdBehaviors = [];
  }

  /**
   * 获取执行统计
   */
  getStats() {
    return {
      ...executionStats,
      successRate: executionStats.totalTasks > 0
        ? (executionStats.successfulTasks / executionStats.totalTasks * 100).toFixed(2) + '%'
        : '0%',
      taskHistory: this.taskHistory.slice(-10)
    };
  }
}

// 导出单例
export const taskBuilder = new TaskBuilder();

// 导出类
export { TaskBuilder };
