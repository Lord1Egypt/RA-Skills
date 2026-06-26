#!/usr/bin/env node

/**
 * 自动识别场景中的夹具并添加行为
 */

import { addBehavior, BehavioralType, ReferenceAxis, getAllModelInfo, getModelTree } from './kunwu-tool.js';

async function autoAddGripperBehaviors() {
  console.log('🔍 自动识别场景中的夹具并添加行为（基于 bounding box 分析）\n');
  
  // 1. 获取所有模型
  const models = await getAllModelInfo();
  const allModels = models.data.models || [];
  
  console.log(`场景中的模型总数：${allModels.length}`);
  
  // 2. 查找夹具相关模型
  const gripperKeywords = ['gripper', 'clamp', '夹爪', '夹具', 'finger', 'mechanical', 'eoat'];
  const gripperModels = allModels.filter(m => {
    const name = m.modelName.toLowerCase();
    return gripperKeywords.some(kw => name.includes(kw));
  });
  
  console.log(`找到夹具相关模型：${gripperModels.length}个\n`);
  
  if (gripperModels.length === 0) {
    console.log('❌ 未找到夹具模型');
    return;
  }
  
  let successCount = 0;
  let failCount = 0;
  let skipCount = 0;
  
  // 3. 为每个夹具添加行为（基于 bounding box 分析）
  for (const model of gripperModels) {
    const name = model.modelName;
    const modelId = model.modelId;
    const modelType = model.modelType;
    const boundSize = model.boundSize || [];
    const transform = model.transform || [];
    
    try {
      // 计算体积
      const volume = boundSize.length >= 3 ? boundSize[0] * boundSize[1] * boundSize[2] : 0;
      const isSmallPart = volume < 100000000;  // 体积小于 1 亿，可能是小部件
      
      // 判断夹具类型
      const isFinger = name.toLowerCase().includes('finger') || 
                       (name.includes('1') || name.includes('2')) && isSmallPart;
      const isBase = name.toLowerCase().includes('base');
      
      // 根据 bounding box 判断运动部件
      const isMovingPart = isSmallPart && !isBase;
      
      if (isFinger && isMovingPart) {
        // 手指：添加直线开合行为
        const isLeft = name.includes('1') || name.includes('left') || 
                       name.includes('finger1');
        const axis = isLeft ? ReferenceAxis.X_NEGATIVE : ReferenceAxis.X_POSITIVE;
        
        // 根据 bounding box 计算合理开度
        const opening = boundSize[0] > 50 ? boundSize[0] / 2 : 25;
        
        console.log(`🔧 ${name}: 检测到手指部件（体积：${volume.toFixed(0)}）`);
        console.log(`   包围盒：${boundSize[0]?.toFixed(1)}×${boundSize[1]?.toFixed(1)}×${boundSize[2]?.toFixed(1)}`);
        console.log(`   添加开合行为（${isLeft ? 'X 负方向' : 'X 正方向'}，开度 0-${opening.toFixed(0)}mm）`);
        
        await addBehavior({
          id: modelId,
          useModeId: true,
          behavioralType: BehavioralType.TRANSLATION,
          referenceAxis: axis,
          minValue: 0,
          maxValue: opening,
          runSpeed: 100,
          isHaveElectricalMachinery: true
        });
        
        console.log(`   ✅ 成功\n`);
        successCount++;
        
      } else if (isBase || !isMovingPart) {
        // 基座或大部件：根据类型决定
        if (modelType === 'EOAT' && !isSmallPart) {
          // 大型 EOAT：可能是整体旋转夹爪
          console.log(`🔧 ${name}: 检测到大型 EOAT（体积：${volume.toFixed(0)}）`);
          console.log(`   包围盒：${boundSize[0]?.toFixed(1)}×${boundSize[1]?.toFixed(1)}×${boundSize[2]?.toFixed(1)}`);
          console.log(`   添加旋转行为（绕 Z 轴，±90°）`);
          
          await addBehavior({
            id: modelId,
            useModeId: true,
            behavioralType: BehavioralType.ROTATE,
            referenceAxis: ReferenceAxis.Z_POSITIVE,
            minValue: -90,
            maxValue: 90,
            runSpeed: 60,
            isHaveElectricalMachinery: true
          });
          
          console.log(`   ✅ 成功\n`);
          successCount++;
        } else {
          console.log(`🔧 ${name}: 基座/固定部件，跳过\n`);
          skipCount++;
        }
      } else {
        console.log(`🔧 ${name}: 无法判断类型，跳过\n`);
        skipCount++;
      }
      
    } catch (error) {
      console.log(`   ❌ 失败：${error.message}\n`);
      failCount++;
    }
  }
  
  // 4. 输出统计
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📊 执行统计:');
  console.log(`  总模型数：${gripperModels.length}`);
  console.log(`  成功：${successCount}`);
  console.log(`  失败：${failCount}`);
  console.log(`  跳过：${skipCount}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  if (successCount > 0) {
    console.log('\n✅ 夹具行为添加完成！');
    console.log('提示：在 Kunwu 软件中切换到"行为信号"模式测试运动');
  }
}

// 执行
autoAddGripperBehaviors().catch(error => {
  console.error('❌ 执行失败:', error.message);
  console.error(error.stack);
  process.exit(1);
});
