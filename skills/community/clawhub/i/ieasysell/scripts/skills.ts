NEW_FILE_CODE
module.exports = {
  name: "Ieasysell 智能外贸业务员（本地拉取版）",
  description: "本地 OpenClaw 定时拉取 Ieasysell 访客管理数据，自动同步记忆 + 实时通知老板，永久接待链接绑定公司数字分身（Token 认证版）",
  version: "0.1.0",
  author: "Ieasysell",

  triggers: [
    "生成智能接待",
    "ieasysell 接待",
    "自动同步客户",
    "实时通知老板",
    "拉取访客记录",
    "数字人接待",
    "重置接待链接"
  ],

  config: {
    ieasysellToken: {
      type: "string",
      label: "Ieasysell 登录 Token",
      required: true,
      description: "在 Ieasysell 网站登录后，从浏览器开发者工具 Application > Local Storage 中获取 token"
    },
    company: { 
      type: "string", 
      label: "公司名称", 
      required: true,
      description: "公司或品牌名称（用于绑定永久接待链接）"
    },
    product: { 
      type: "string", 
      label: "主营产品", 
      required: true,
      description: "公司主营产品或服务描述"
    },
    market: {
      type: "string",
      label: "目标市场",
      required: false,
      default: "global",
      description: "目标市场/国家，如：美国、欧洲、东南亚等"
    },
    syncInterval: {
      type: "number",
      label: "同步间隔（分钟）",
      required: false,
      default: 5,
      description: "定时拉取访客记录的间隔时间（默认 5 分钟）"
    }
  },

  async run(claw, args, config) {
    const { ieasysellToken, company, product, market = "global", syncInterval = 5 } = config;
    const memory = claw.memory || {};
    const lastSyncTime = memory.last_sync_time || 0;
    const syncIntervalMs = syncInterval * 60 * 1000; // 转换为毫秒

    // 判断是否是重置操作
    const isReset = args.includes("重置") || args.includes("reset") || args.includes("重新生成");

    // 1. 从 OpenClaw 本地记忆获取优化 Prompt
    const optimizedPrompt = memory.reception_prompt || `
你是专业外贸数字人 AI 销售员，具备以下能力：
- 多语种接待（中文、英文等）
- 专业介绍${company}的${product}产品
- 引导客户留下联系方式（邮箱、电话、WhatsApp 等）
- 锁客防流失，提高转化率
- 根据客户意向等级提供差异化服务
`;

    try {
      // ==============================================
      // 2. 验证 Token 并获取租户信息
      // ==============================================
      
      await claw.say(`
🔐 正在验证登录状态...
• 公司：${company}
• 产品：${product}
• 目标市场：${market}
      `);

      const tenantInfo = await getTenantInfo(ieasysellToken);
      if (!tenantInfo) {
        throw new Error('Token 验证失败，请检查 Token 是否有效或已过期');
      }

      await claw.say(`✅ 登录验证成功\n• 租户 ID：${tenantInfo.tenantId}\n• 用户名：${tenantInfo.username}`);

      // ==============================================
      // 3. 核心逻辑：优先查询已有数字分身，无则新建，有则更新配置
      // ==============================================
      
      await claw.say(`
🔍 正在处理你的 AI 业务员配置...
• 操作类型：${isReset ? '🔄 重置并生成新链接' : '✨ 创建/更新接待链接'}
      `);

      let receptionUrl;
      let digitalHumanId;
      let isNewCreation = false;

      if (isReset) {
        // 用户主动重置：直接生成新数字分身（旧链接自动失效）
        await claw.say(`⚠️ 正在重置你的接待链接，旧链接将自动失效...`);
        
        const createRes = await fetch("https://crm.ieasysell.com/client/digitalHuman/create", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${ieasysellToken}`
          },
          body: JSON.stringify({
            name: `${company}智能业务员`,
            company,
            product,
            market,
            prompt: optimizedPrompt,
            forceCreateNew: true // 强制创建新分身
          })
        });

        if (!createRes.ok) {
          throw new Error(`HTTP error! status: ${createRes.status}`);
        }

        const { code, data, message } = await createRes.json();
        
        if (code !== 200) {
          throw new Error(message || '重置接待链接失败');
        }

        digitalHumanId = data.id;
        receptionUrl = data.liveUrl || data.url;
        isNewCreation = true;

        await claw.say(`
✅ 已重置你的 AI 业务员接待链接（新链接已生效）：
${receptionUrl}

⚠️ 重要提醒：
• 旧链接已自动失效，请立即更新独立站/推广渠道的配置
• 历史访客数据已迁移到新分身
• 请尽快将新链接告知客户
        `);

      } else {
        // 正常流程：优先查询已有数字分身
        const queryRes = await fetch("https://crm.ieasysell.com/client/digitalHuman/list", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${ieasysellToken}`
          },
          query: { 
            tenantId: tenantInfo.tenantId
          }
        });

        if (!queryRes.ok) {
          throw new Error(`查询数字分身失败：HTTP ${queryRes.status}`);
        }

        const { code, data, message } = await queryRes.json();
        
        if (code !== 200 && code !== 404) {
          throw new Error(message || '查询数字分身失败');
        }

        // 查找匹配的数字分身
        const existingDigitalHuman = data?.list?.find(dh => dh.company === company);

        if (existingDigitalHuman) {
          // 已有数字分身：更新配置（提示词）
          digitalHumanId = existingDigitalHuman.id;
          
          await claw.say(`📝 检测到你的公司已有数字分身，正在更新智能体配置...`);

          const updateRes = await fetch(`https://crm.ieasysell.com/client/digitalHuman/update/${digitalHumanId}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${ieasysellToken}`
            },
            body: JSON.stringify({
              id: digitalHumanId,
              name: existingDigitalHuman.name || `${company}智能业务员`,
              company,
              product,
              market,
              prompt: optimizedPrompt,
              roleSetting: optimizedPrompt, // 角色设定（数字分身配置）
              updatedAt: Date.now()
            })
          });

          if (!updateRes.ok) {
            throw new Error(`更新数字分身配置失败：HTTP ${updateRes.status}`);
          }

          const { code: updateCode, data: updateData, message: updateMessage } = await updateRes.json();
          
          if (updateCode !== 200) {
            throw new Error(updateMessage || '更新数字分身配置失败');
          }

          receptionUrl = updateData.liveUrl || updateData.url || existingDigitalHuman.url;

          await claw.say(`
✅ 已更新你的 AI 业务员接待配置（链接不变）：
${receptionUrl}

📊 更新内容：
• 数字分身 ID：${digitalHumanId}
• 提示词/话术：已基于历史访客记录优化
• 产品描述：${product}
• 目标市场：${market}
• 更新时间：${new Date().toLocaleString()}

💡 优势：
• 链接永久有效，无需频繁更新配置
• 历史访客数据完整保留（访客管理菜单可查看）
• AI 越接待越聪明（持续学习优化）
          `);

        } else {
          // 无数字分身：新建数字分身 + 生成永久链接
          await claw.say(`🆕 未检测到你的数字分身，正在创建专属 AI 智能体...`);

          const createRes = await fetch("https://crm.ieasysell.com/client/digitalHuman/create", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${ieasysellToken}`
            },
            body: JSON.stringify({
              name: `${company}智能业务员`,
              company,
              product,
              market,
              prompt: optimizedPrompt,
              roleSetting: optimizedPrompt // 角色设定（数字分身配置）
            })
          });

          if (!createRes.ok) {
            throw new Error(`创建数字分身失败：HTTP ${createRes.status}`);
          }

          const { code: createCode, data: createData, message: createMessage } = await createRes.json();
          
          if (createCode !== 200) {
            throw new Error(createMessage || '创建数字分身失败');
          }

          digitalHumanId = createData.id;
          receptionUrl = createData.liveUrl || createData.url;
          isNewCreation = true;

          await claw.say(`
🎉 已为你创建专属 AI 业务员数字分身（永久有效）：
${receptionUrl}

📋 配置信息：
• 分身名称：${createData.name || `${company}智能业务员`}
• 分身 ID：${digitalHumanId}
• 公司名称：${company}
• 主营产品：${product}
• 目标市场：${market}
• 创建时间：${new Date().toLocaleString()}

💡 使用说明：
• 将链接嵌入独立站右下角
• 发送给需要咨询的客户
• 链接永久有效，无需更换
• 可在「数字分身」菜单管理配置
• AI 会自动学习优化，越用越聪明
          `);
        }
      }

      // ==============================================
      // 4. 启动本地定时拉取（从访客管理菜单拉取数据）
      // ==============================================
      
      const startSyncLoop = async () => {
        try {
          console.log(`[${new Date().toLocaleString()}] 开始同步访客管理数据...`);
          
          // 从访客管理 API 拉取新访客记录
          const syncRes = await fetch("https://crm.ieasysell.com/client/websocket/visitorInfo/getVisitorInfoListByTenantId", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${ieasysellToken}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              tenantId: tenantInfo.tenantId,
              digitalHumanId: digitalHumanId // 传递数字分身 ID，确保拉取对应数据
            })
          });

          if (!syncRes.ok) {
            console.error('同步请求失败:', syncRes.status);
            return;
          }

          const { code, data } = await syncRes.json();
          
          if (code !== 200) {
            console.error('同步返回错误:', data);
            return;
          }

          const newVisitors = data.list || data.visitors || data.records || [];

          // 只处理新记录
          const newRecords = newVisitors.filter(visitor => {
            const visitorTime = new Date(visitor.createTime || visitor.latestVisitTime).getTime();
            return visitorTime > lastSyncTime;
          });

          if (newRecords.length > 0) {
            console.log(`发现${newRecords.length}个新访客`);
            
            // 更新本地记忆
            const updatedMemory = {
              last_sync_time: Date.now(),
              visitor_count: (memory.visitor_count || 0) + newRecords.length,
              reception_prompt: await optimizePromptFromVisitors(claw, newRecords),
              last_visitors: newRecords.slice(0, 10), // 保存最近 10 个访客
              company: company,
              digitalHumanId: digitalHumanId,
              tenantId: tenantInfo.tenantId
            };
            
            await claw.updateMemory(updatedMemory);

            // 本地通知用户（每个新访客都通知）
            for (const visitor of newRecords) {
              const notification = buildVisitorNotification(visitor);
              await claw.notifyUser(notification);
              
              // 短暂延迟避免通知刷屏
              await sleep(1000);
            }

            await claw.say(`
📊 同步完成报告：
• 新增访客：${newRecords.length} 人
• 累计访客：${updatedMemory.visitor_count} 人
• 最新同步：${new Date(updatedMemory.last_sync_time).toLocaleString()}
• 话术已自动优化
            `);
          } else {
            console.log('没有新的访客记录');
          }
        } catch (error) {
          console.error('定时同步出错:', error);
          // 不在这里通知用户，避免频繁打扰
        }
      };

      // 立即执行一次同步
      await startSyncLoop();

      // 启动定时任务
      setInterval(startSyncLoop, syncIntervalMs);

      return { 
        success: true, 
        reception_url: receptionUrl,
        digital_human_id: digitalHumanId,
        is_new_creation: isNewCreation,
        message: isReset 
          ? '已重置接待链接' 
          : isNewCreation 
            ? '已创建永久接待链接' 
            : '已更新接待配置'
      };

    } catch (error) {
      console.error('Skill 执行出错:', error);
      await claw.say(`
❌ 初始化失败
错误原因：${error.message}

请检查：
1. Token 是否有效（从浏览器开发者工具获取）
2. 网络连接是否正常
3. 公司名称是否准确（区分大小写）
4. Ieasysell 账户是否有效

📖 获取 Token 步骤：
1. 打开浏览器访问 https://app.ieasysell.com
2. 登录你的账户
3. 按 F12 打开开发者工具
4. 点击 Application > Local Storage
5. 找到 token 字段，复制其值
6. 粘贴到 OpenClaw 配置中

如需重置接待链接，请使用触发词："重置接待链接"
      `);
      
      return { 
        success: false, 
        error: error.message 
      };
    }
  }
};

// ============================================
// 辅助函数
// ============================================

/**
 * 获取租户信息（通过 Token）
 */
async function getTenantInfo(token) {
  try {
    const res = await fetch("https://crm.ieasysell.com/client/account/info", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });
    
    if (res.ok) {
      const { data } = await res.json();
      return {
        tenantId: data.tenantId || data.tenant_id,
        username: data.username || data.name,
        email: data.email
      };
    } else {
      console.error('获取租户信息失败:', res.status);
    }
  } catch (error) {
    console.error('获取租户 ID 失败:', error);
  }
  
  return null;
}

/**
 * 根据访客记录优化 Prompt
 */
async function optimizePromptFromVisitors(claw, visitors) {
  // 分析访客特征
  const countries = new Set();
  const languages = new Set();
  const intentionDistribution = { HIGH: 0, MEDIUM: 0, LOW: 0 };
  
  visitors.forEach(visitor => {
    if (visitor.countryCode) countries.add(visitor.countryCode);
    if (visitor.language) languages.add(visitor.language);
    if (visitor.intentionLevel) {
      intentionDistribution[visitor.intentionLevel] = (intentionDistribution[visitor.intentionLevel] || 0) + 1;
    }
  });

  // 生成优化后的 Prompt
  const totalVisitors = visitors.length;
  const basePrompt = `你是专业外贸数字人 AI 销售员，服务于本公司。

核心能力：
1. 多语种接待：支持${Array.from(languages).join('、') || '多国语言'}
2. 区域化服务：主要客户来自${Array.from(countries).join('、') || '多个国家'}
3. 智能问答：熟练回答客户关心的问题
4. 留资引导：巧妙引导客户留下联系方式
5. 意向判断：准确识别客户意向等级

访客数据分析（最近${totalVisitors}人）：
- 高意向客户：${intentionDistribution.HIGH || 0}人
- 中意向客户：${intentionDistribution.MEDIUM || 0}人
- 低意向客户：${intentionDistribution.LOW || 0}人

接待策略：
- 高意向客户：重点跟进，快速响应，优先留资
- 中意向客户：耐心解答，建立信任，逐步引导
- 低意向客户：保持互动，提供价值，培养意向

持续学习：每次接待后自动优化话术，越接待越聪明！
`;

  return basePrompt;
}

/**
 * 构建访客通知消息
 */
function buildVisitorNotification(visitor) {
  const intentionEmoji = {
    'HIGH': '🔥',
    'MEDIUM': '⭐',
    'LOW': '💡'
  };

  const intentionText = {
    'HIGH': '高意向',
    'MEDIUM': '中意向',
    'LOW': '低意向'
  };

  const countryName = visitor.countryName || visitor.countryCode || '未知国家';
  const visitCount = visitor.visitCount || 1;
  const messageCount = visitor.totalMessageCount || 0;
  
  // 提取联系方式
  let contactInfo = '暂无';
  if (visitor.contactInfo) {
    const contacts = [];
    if (visitor.contactInfo.email && visitor.contactInfo.email.length > 0) {
      contacts.push(`📧 ${visitor.contactInfo.email.join(', ')}`);
    }
    if (visitor.contactInfo.phone && visitor.contactInfo.phone.length > 0) {
      contacts.push(`📱 ${visitor.contactInfo.phone.join(', ')}`);
    }
    if (visitor.contactInfo.whatsapp && visitor.contactInfo.whatsapp.length > 0) {
      contacts.push(`💬 ${visitor.contactInfo.whatsapp.join(', ')}`);
    }
    if (contacts.length > 0) {
      contactInfo = contacts.join('\n');
    }
  }

  return `
📩 新访客访问通知
━━━━━━━━━━━━━━━━━━━━
👤 访客：${visitor.name || '匿名访客'} 
🌍 地区：${countryName}
🎯 意向：${intentionEmoji[visitor.intentionLevel] || '💼'} ${intentionText[visitor.intentionLevel] || visitor.intentionLevel || '未评估'}
📊 数据：访问${visitCount}次 | 消息${messageCount}条

📞 联系方式：
${contactInfo}

💡 建议：
${generateVisitorSuggestion(visitor)}

✅ 已自动优化话术
━━━━━━━━━━━━━━━━━━━━
  `.trim();
}

/**
 * 生成跟进建议
 */
function generateVisitorSuggestion(visitor) {
  const suggestions = [];
  
  if (visitor.intentionLevel === 'HIGH') {
    suggestions.push('🔥 高意向客户，建议立即人工跟进');
    if (!visitor.contactInfo || Object.keys(visitor.contactInfo || {}).length === 0) {
      suggestions.push('⚠️ 尚未留资，需重点引导获取联系方式');
    }
  } else if (visitor.intentionLevel === 'MEDIUM') {
    suggestions.push('⭐ 中意向客户，保持互动建立信任');
    suggestions.push('💬 主动解答疑问，展示专业度');
  } else {
    suggestions.push('💡 低意向客户，提供有价值内容培养兴趣');
    suggestions.push('⏰ 定期跟进，不要过于频繁');
  }

  if (visitor.visitCount > 3) {
    suggestions.push('🔄 多次访问客户，对产品有持续兴趣');
  }

  if (visitor.totalMessageCount > 10) {
    suggestions.push('💬 深度交流客户，已建立初步信任');
  }

  return suggestions.join('\n');
}

/**
 * 延迟函数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}