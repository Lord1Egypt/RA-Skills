import { getApiKey, httpsRequest, API_HOST, log, colors, success, error, info, safeJsonParse } from '../utils.js';

export async function listChachas(options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  const searchKeyword = options.search || options._search;
  if (searchKeyword) {
    info(`正在搜索包含 "${searchKeyword}" 的查查...`);
  } else {
    info('正在获取查查列表...');
  }

  const query = `
    query GetChachas($limit: Int, $skip: Int, $title: String, $_search: String) {
      chachas(limit: $limit, skip: $skip, title: $title, _search: $_search, isRemove: false) {
        _id
        title
        content
        sharePoster
        authorName
        wxLogo
        isNewForm
        sheets {
          id
          title
          headers
        }
        createdAt
      }
    }
`;

  const variables = {
    limit: options.limit ? parseInt(options.limit) : 50,
    skip: options.skip ? parseInt(options.skip) : 0
  };

  if (options.title) {
    variables.title = options.title;
  }
  if (searchKeyword) {
    variables._search = searchKeyword;
  }

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
        operationName: 'chachas'
      })
    );

    let chachas = null;
    if (Array.isArray(response.data)) {
      chachas = response.data;
    } else if (response.data && response.data.chachas) {
      chachas = response.data.chachas;
    }

    if (chachas) {
      success(`找到 ${chachas.length} 个查查`);
      chachas.forEach((chacha, index) => {
        log(colors.bright, `${index + 1}. ${chacha.title}`);
        log(colors.cyan, `   ID: ${chacha._id}`);
        if (chacha.content)
          log(
            colors.cyan,
            `   描述: ${chacha.content.substring(0, 100)}${chacha.content.length > 100 ? '...' : ''}`
          );
        if (chacha.authorName) log(colors.cyan, `   作者: ${chacha.authorName}`);
        if (chacha.isNewForm !== undefined)
          log(colors.cyan, `   新表单: ${chacha.isNewForm ? '是' : '否'}`);
        if (chacha.sheets && chacha.sheets.length > 0) {
          log(colors.cyan, `   表格数: ${chacha.sheets.length}`);
          chacha.sheets.forEach((sheet, idx) => {
            log(
              colors.cyan,
              `     ${idx + 1}. ${sheet.title || '未命名'} (${sheet.headers?.length || 0} 列)`
            );
          });
        }
        log(colors.cyan, `   创建时间: ${new Date(chacha.createdAt).toLocaleString('zh-CN')}`);
        console.log('');
      });

      return chachas;
    } else {
      throw new Error('获取查查列表失败');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

export async function updateChacha(options) {
  const apiKey = getApiKey(options?.apiKey);

  if (!options.id) {
    error('请提供查查 ID (--id 参数)');
    process.exit(1);
  }

  const formConfig = {
    _id: options.id
  };

  if (options.title) formConfig.title = options.title;
  if (options.desc) formConfig.content = options.desc;
  if (options.authorName) formConfig.authorName = options.authorName;
  if (options.sheets) {
    try {
      formConfig.sheets = typeof options.sheets === 'string'
        ? safeJsonParse(options.sheets, 'sheets')
        : options.sheets;
    } catch (err) {
      error(`表格配置解析失败: ${err.message}`);
      info('请确保 --sheets 参数是有效的 JSON 数组格式');
      process.exit(1);
    }
  }

  info('正在更新查查...');

  const mutation = `
  mutation UpdateChacha($input: updateChachaInput!) {
    updateChachaByInput(input: $input) {
      _id
      title
      content
      authorName
      isNewForm
      sheets {
        id
        title
        headers
      }
    }
  }
`;

  const data = JSON.stringify({
    query: mutation,
    variables: { input: formConfig },
    operationName: 'updateChachaByInput'
  });

  try {
    const response = await httpsRequest(
      {
        hostname: API_HOST,
        port: 443,
        path: '/api/openapi/graphql',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
          'Content-Length': Buffer.byteLength(data)
        }
      },
      data
    );

    if (response.errors) {
      error('GraphQL 错误:', JSON.stringify(response.errors));
      process.exit(1);
    }

    const result = response.data.updateChachaByInput || response.data;
    if (result && result._id) {
      success('查查更新成功！');
      log(colors.bright, '   ID:', result._id);
      log(colors.bright, '   标题:', result.title);
      if (result.isNewForm !== undefined) {
        log(colors.bright, '   新表单:', result.isNewForm ? '是' : '否');
      }
      return result._id;
    } else {
      error('响应格式异常:', JSON.stringify(response));
      process.exit(1);
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

export async function getChacha(chachaId, options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  info(`正在获取查查 ${chachaId} 的详情...`);

  const query = `
    query GetChachas($_id: ID) {
      chachas(_id: $_id, isRemove: false) {
        _id
        title
        content
        sharePoster
        authorName
        wxLogo
        managers
        isNewForm
        sheets {
          id
          title
          headers
          searchConditionSettings
          allowChangeKeys
          hideKeys
          needConfirm
          confirmType
          limitQueryCount
          limitQueryTime
          startTime
          endTime
          imageSearchRules {
            headerIndex
            headerName
            values
            images
          }
        }
        createdAt
      }
    }
`;

  const variables = {
    _id: chachaId
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
        operationName: 'chachas'
      })
    );

    let chachas = null;
    if (Array.isArray(response.data)) {
      chachas = response.data;
    } else if (response.data && response.data.chachas) {
      chachas = response.data.chachas;
    }

    if (chachas && chachas.length > 0) {
      const chacha = chachas[0];
      success('查查详情');
      log(colors.bright, `   ID: ${chacha._id}`);
      log(colors.bright, `   标题: ${chacha.title}`);
      if (chacha.content)
        log(
          colors.cyan,
          `   描述: ${chacha.content.substring(0, 200)}${chacha.content.length > 200 ? '...' : ''}`
        );
      if (chacha.authorName) log(colors.cyan, `   作者: ${chacha.authorName}`);
      if (chacha.managers && chacha.managers.length > 0)
        log(colors.cyan, `   管理员: ${chacha.managers.length} 人`);
      if (chacha.isNewForm !== undefined)
        log(colors.cyan, `   新表单: ${chacha.isNewForm ? '是' : '否'}`);
      log(colors.cyan, `   创建时间: ${new Date(chacha.createdAt).toLocaleString('zh-CN')}`);

      if (chacha.sheets && chacha.sheets.length > 0) {
        log(colors.cyan, `   表格 (${chacha.sheets.length} 个):`);
        chacha.sheets.forEach((sheet, index) => {
          log(colors.cyan, `     ${index + 1}. ${sheet.title || '未命名'}`);
          if (sheet.headers && sheet.headers.length > 0) {
            log(colors.cyan, `        表头: ${sheet.headers.join(', ')}`);
          }
          if (sheet.searchConditionSettings && sheet.searchConditionSettings.length > 0) {
            const conditionHeaders = sheet.searchConditionSettings
              .map(idx => sheet.headers[idx])
              .join(', ');
            log(colors.cyan, `        查询条件: ${conditionHeaders}`);
          }
          if (sheet.limitQueryCount && sheet.limitQueryCount > 0) {
            log(colors.cyan, `        查询限制: 每个微信号仅可查 ${sheet.limitQueryCount} 条`);
          }
          if (sheet.limitQueryTime) {
            log(
              colors.cyan,
              `        时间限制: ${new Date(sheet.startTime).toLocaleString('zh-CN')} - ${new Date(sheet.endTime).toLocaleString('zh-CN')}`
            );
          }
          if (sheet.imageSearchRules && sheet.imageSearchRules.length > 0) {
            log(colors.cyan, `        图片搜索规则: ${sheet.imageSearchRules.length} 条`);
            sheet.imageSearchRules.forEach((rule, ruleIdx) => {
              log(
                colors.cyan,
                `          ${ruleIdx + 1}. ${rule.headerName}: ${rule.values?.join(', ') || '无'} (${rule.images?.length || 0} 张图片)`
              );
            });
          }
        });
      }

      return chacha;
    } else {
      throw new Error('未找到该查查');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}
