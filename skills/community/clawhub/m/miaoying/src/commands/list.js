import { getApiKey, httpsRequest, API_HOST, log, colors, success, error, info } from '../utils.js';

export async function listTongjis(options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  const searchKeyword = options.search || options._search;
  if (searchKeyword) {
    info(`正在搜索包含 "${searchKeyword}" 的统计...`);
  } else {
    info('正在获取统计列表...');
  }

  const query = `
    query GetTongjis($limit: Int, $skip: Int, $title: String, $_search: String) {
      tongjis(limit: $limit, skip: $skip, title: $title, _search: $_search, isRemove: false) {
        _id
        title
        content
        createdAt
        resultsCount
        count
        totalAllow
      }
    }
`;

  const variables = {
    limit: options.limit ? parseInt(options.limit) : 50,
    skip: options.skip ? parseInt(options.skip) : 0,
    title: options.title || undefined,
    _search: searchKeyword || undefined
  };

  try {
    const response = await httpsRequest(
      {
        hostname: API_HOST,
        port: 443,
        path: '/api/openapi/graphql',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`
        }
      },
      JSON.stringify({
        query,
        variables,
        operationName: 'tongjis'
      })
    );

    let tongjis = null;
    if (Array.isArray(response.data)) {
      tongjis = response.data;
    } else if (response.data && response.data.tongjis) {
      tongjis = response.data.tongjis;
    }

    if (tongjis) {
      success(`找到 ${tongjis.length} 个统计`);
      console.log('');

      tongjis.forEach((tongji, index) => {
        log(colors.bright, `${index + 1}. ${tongji.title}`);
        log(colors.cyan, `   ID: ${tongji._id}`);
        log(
          colors.cyan,
          `   报名数: ${tongji.resultsCount || 0}/${tongji.totalAllow || tongji.count || '不限'}`
        );
        log(colors.cyan, `   创建时间: ${new Date(tongji.createdAt).toLocaleString('zh-CN')}`);
        console.log('');
      });

      return tongjis;
    } else {
      throw new Error('获取统计列表失败');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

export async function getTongji(tongjiId, options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  info(`正在获取统计 ${tongjiId} 的详情...`);

  const query = `
    query GetTongjis($_id: ID) {
      tongjis(_id: $_id, isRemove: false) {
        _id
        title
        content
        createdAt
        resultsCount
        count
        totalAllow
        isSelectCourse
        needExamMode
        needInfo
        infoForms {
          id
          type
          title
          required
          options
          courseSetting {
            id
            title
            quota
            schedule {
              dayOfWeek
              startTime
              endTime
            }
            teacher
            location
            price
          }
        }
        isAnonymous
        isRepeat
        endTime
        cover
        pictures
        needBookMode
        dayRepeatCount
        allowSubmitTimeRules {
          startTime
          endTime
        }
      }
    }
`;

  const variables = {
    _id: tongjiId
  };

  try {
    const response = await httpsRequest(
      {
        hostname: API_HOST,
        port: 443,
        path: '/api/openapi/graphql',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`
        }
      },
      JSON.stringify({
        query,
        variables,
        operationName: 'tongjis'
      })
    );

    let tongjis = null;
    if (Array.isArray(response.data)) {
      tongjis = response.data;
    } else if (response.data && response.data.tongjis) {
      tongjis = response.data.tongjis;
    }

    if (tongjis && tongjis.length > 0) {
      const tongji = tongjis[0];
      success('统计详情');
      log(colors.bright, `   ID: ${tongji._id}`);
      log(colors.bright, `   标题: ${tongji.title}`);
      if (tongji.content)
        log(
          colors.cyan,
          `   描述: ${tongji.content.substring(0, 100)}${tongji.content.length > 100 ? '...' : ''}`
        );
      log(
        colors.cyan,
        `   报名数: ${tongji.resultsCount || 0}/${tongji.totalAllow || tongji.count || '不限'}`
      );
      log(colors.cyan, `   创建时间: ${new Date(tongji.createdAt).toLocaleString('zh-CN')}`);
      if (tongji.endTime)
        log(colors.cyan, `   结束时间: ${new Date(tongji.endTime).toLocaleString('zh-CN')}`);
      if (tongji.isAnonymous) log(colors.cyan, `   匿名填写: 是`);
      if (tongji.isRepeat) log(colors.cyan, `   重复打卡: 是`);
      if (tongji.isSelectCourse) log(colors.cyan, `   选课模式: 是`);
      if (tongji.needExamMode) log(colors.cyan, `   考试模式: 是`);
      if (tongji.needInfo) log(colors.cyan, `   信息收集: 是`);
      if (tongji.needBookMode) log(colors.cyan, `   预约模式: 是`);
      if (tongji.dayRepeatCount) log(colors.cyan, `   每天时段数: ${tongji.dayRepeatCount}`);
      if (tongji.allowSubmitTimeRules && tongji.allowSubmitTimeRules.length > 0) {
        log(colors.cyan, `   预约时段:`);
        tongji.allowSubmitTimeRules.forEach((rule, index) => {
          log(colors.cyan, `     ${index + 1}. ${rule.startTime} - ${rule.endTime}`);
        });
      }
      if (tongji.infoForms && tongji.infoForms.length > 0) {
        log(colors.cyan, `   表单字段 (${tongji.infoForms.length} 个):`);
        tongji.infoForms.forEach((form, index) => {
          const requiredStr = form.required ? '(必填)' : '';
          if (form.type === '24' && form.courseSetting) {
            log(
              colors.cyan,
              `     ${index + 1}. ${form.title} ${requiredStr}[类型: 24 - 课程选择]`
            );
            log(colors.cyan, `        可选课程 (${form.courseSetting.length} 门):`);
            form.courseSetting.forEach((course, idx) => {
              const scheduleInfo =
                course.schedule && course.schedule.length > 0
                  ? course.schedule
                      .map(s => {
                        const dayMap = {
                          1: '周一',
                          2: '周二',
                          3: '周三',
                          4: '周四',
                          5: '周五',
                          6: '周六',
                          7: '周日'
                        };
                        const day = dayMap[s.dayOfWeek] || s.dayOfWeek;
                        return `${day} ${s.startTime}-${s.endTime}${course.location ? '@' + course.location : ''}`;
                      })
                      .join('; ')
                  : '';
              log(
                colors.cyan,
                `          ${idx + 1}. ${course.title} (配额:${course.quota}) ${scheduleInfo ? '[' + scheduleInfo + ']' : ''}`
              );
            });
          } else {
            const optionsStr = form.options ? ` [选项: ${form.options.join(', ')}]` : '';
            log(
              colors.cyan,
              `     ${index + 1}. ${form.title} ${requiredStr}[类型: ${form.type}]${optionsStr}`
            );
          }
        });
      }

      return tongji;
    } else {
      throw new Error('未找到该统计');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

export async function getBaomingsTotals(tongjiId, options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  info(`正在获取统计 ${tongjiId} 的报名总数...`);

  const query = `
    query GetBaomingsTotals($tongjiId: String) {
      getBaomingsTotals(tongjiId: $tongjiId) {
        total
        passTotal
        checkedTotal
        uncheckTotal
      }
    }
`;

  const variables = {
    tongjiId: tongjiId
  };

  try {
    const response = await httpsRequest(
      {
        hostname: API_HOST,
        port: 443,
        path: '/api/openapi/graphql',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`
        }
      },
      JSON.stringify({
        query,
        variables,
        operationName: 'getBaomingsTotals'
      })
    );

    let totals = null;
    if (response.data && typeof response.data === 'object' && !Array.isArray(response.data)) {
      if ('total' in response.data || 'passTotal' in response.data) {
        totals = response.data;
      } else if (response.data.getBaomingsTotals) {
        totals = response.data.getBaomingsTotals;
      }
    }

    if (totals) {
      success('报名统计');
      log(colors.bright, `   总数: ${totals.total || 0}`);
      log(colors.bright, `   通过: ${totals.passTotal || 0}`);
      log(colors.bright, `   已审核: ${totals.checkedTotal || 0}`);
      log(colors.bright, `   未审核: ${totals.uncheckTotal || 0}`);

      return totals;
    } else {
      throw new Error('获取报名总数失败');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

export async function getBaomings(tongjiId, options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  info(`正在获取统计 ${tongjiId} 的报名结果...`);

  const query = `
    query GetBaomings($tongjiId: String, $limit: Int, $skip: Int) {
      baomings(tongjiId: $tongjiId, limit: $limit, skip: $skip) {
        _id
        createdAt
        results
        userId
        userName
        submitTime
        no
        noLabel
      }
    }
`;

  const variables = {
    tongjiId: tongjiId,
    limit: options.limit ? parseInt(options.limit) : 20,
    skip: options.skip ? parseInt(options.skip) : 0
  };

  try {
    const response = await httpsRequest(
      {
        hostname: API_HOST,
        port: 443,
        path: '/api/openapi/graphql',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`
        }
      },
      JSON.stringify({
        query,
        variables,
        operationName: 'baomings'
      })
    );

    let baomings = null;
    if (Array.isArray(response.data)) {
      baomings = response.data;
    } else if (response.data && response.data.baomings) {
      baomings = response.data.baomings;
    }

    if (baomings) {
      success(`获取到 ${baomings.length} 条报名记录`);
      console.log('');

      baomings.forEach((baoming, index) => {
        const name = baoming.userName || baoming.userId || '未知';
        const time = baoming.submitTime
          ? new Date(baoming.submitTime).toLocaleString('zh-CN')
          : '-';
        log(colors.bright, `${index + 1}. ${name}`);
        log(colors.cyan, `   ID: ${baoming._id}`);
        log(colors.cyan, `   提交时间: ${time}`);
        if (baoming.no !== undefined) log(colors.cyan, `   序号: ${baoming.no}`);
        if (baoming.results) {
          const results =
            typeof baoming.results === 'string' ? baoming.results : JSON.stringify(baoming.results);
          log(
            colors.cyan,
            `   结果: ${results.substring(0, 50)}${results.length > 50 ? '...' : ''}`
          );
        }
        console.log('');
      });

      return baomings;
    } else {
      throw new Error('获取报名结果失败');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}
