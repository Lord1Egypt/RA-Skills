import { getApiKey, httpsRequest, API_HOST, log, colors, success, error, info, safeJsonParse } from '../utils.js';

function getDefaultOptionForms() {
  return [
    {
      id: Date.now().toString(),
      title: '投票标题',
      required: true,
      options: [
        { title: '选项1', isImage: false, imageUrl: '' },
        { title: '选项2', isImage: false, imageUrl: '' },
        { title: '选项3', isImage: false, imageUrl: '' },
        { title: '选项4', isImage: false, imageUrl: '' }
      ],
      optionAllowOther: false,
      singleOption: false
    }
  ];
}

export async function createToupiao(options) {
  const apiKey = getApiKey(options?.apiKey);

  // Safely parse options JSON
  let optionForms;
  if (options.options) {
    try {
      optionForms = safeJsonParse(options.options, 'options');
    } catch (err) {
      error(`投票选项解析失败: ${err.message}`);
      info('请确保 --options 参数是有效的 JSON 数组格式');
      process.exit(1);
    }
  } else {
    optionForms = getDefaultOptionForms();
  }

  const formConfig = {
    title: options.title || '未命名投票',
    content: options.desc || '',
    singleOption: options.single ? true : false,
    startTime: options.startTime ? new Date(options.startTime).getTime() : new Date().getTime(),
    endTime: options.endTime
      ? new Date(options.endTime).getTime()
      : new Date().getTime() + 7 * 24 * 3600 * 1000,
    optionForms: optionForms,
    isMultiOptions: true,
    publishResult: options.publishResult !== undefined ? options.publishResult === 'true' : true,
    isAnonymous: options.anonymous === 'true'
  };

  if (options.count) formConfig.count = parseInt(options.count);
  if (options.limitCount) formConfig.limitCount = true;
  if (options.allowVoteCount) formConfig.allowVoteCount = parseInt(options.allowVoteCount);
  if (options.minSelect) formConfig.minSelect = parseInt(options.minSelect);
  if (options.maxSelect) formConfig.maxSelect = parseInt(options.maxSelect);
  if (options.optionAllowOther) formConfig.optionAllowOther = true;

  info('正在创建投票...');

  const mutation = `
  mutation CreateToupiao($input: createToupiaoInput!) {
    createToupiaoByInput(input: $input) {
      _id
      title
      createdAt
      singleOption
      optionForms {
        title
        options {
          title
        }
      }
    }
  }
`;

  const data = JSON.stringify({
    query: mutation,
    variables: { input: formConfig },
    operationName: 'createToupiaoByInput'
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

    if (response.data && response.data._id) {
      success('投票创建成功！');
      log(colors.bright, '   ID:', response.data._id);
      log(colors.bright, '   标题:', response.data.title);
      log(colors.bright, '   类型:', response.data.singleOption ? '单选' : '多选');
      log(colors.bright, '   选项数:', response.data.optionForms?.length || 0);

      if (options.qrcode) {
        info('正在生成二维码...');
        const { generateToupiaoQrCode } = await import('./qrcode.js');
        await generateToupiaoQrCode(response.data._id, options);
      } else {
        info('使用以下命令生成二维码:');
        log(colors.cyan, `   miaoying toupiao-qrcode ${response.data._id}`);
      }

      return response.data._id;
    } else {
      error('响应格式异常:', JSON.stringify(response));
      process.exit(1);
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

export async function listToupiaos(options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  const searchKeyword = options.search || options._search;
  if (searchKeyword) {
    info(`正在搜索包含 "${searchKeyword}" 的投票...`);
  } else {
    info('正在获取投票列表...');
  }

  const query = `
    query GetToupiaos($limit: Int, $skip: Int, $title: String, $_search: String) {
      toupiaos(limit: $limit, skip: $skip, title: $title, _search: $_search, isRemove: false) {
        _id
        title
        content
        createdAt
        singleOption
        allowVoteCount
        voteTimeType
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
        operationName: 'toupiaos'
      })
    );

    let toupiaos = null;
    if (Array.isArray(response.data)) {
      toupiaos = response.data;
    } else if (response.data && response.data.toupiaos) {
      toupiaos = response.data.toupiaos;
    }

    if (toupiaos) {
      success(`找到 ${toupiaos.length} 个投票`);
      console.log('');

      toupiaos.forEach((toupiao, index) => {
        log(colors.bright, `${index + 1}. ${toupiao.title}`);
        log(colors.cyan, `   ID: ${toupiao._id}`);
        log(colors.cyan, `   类型: ${toupiao.singleOption ? '单选' : '多选'}`);
        if (toupiao.allowVoteCount)
          log(
            colors.cyan,
            `   投票次数: ${toupiao.voteTimeType || '总共'} ${toupiao.allowVoteCount}次`
          );
        log(colors.cyan, `   创建时间: ${new Date(toupiao.createdAt).toLocaleString('zh-CN')}`);
        console.log('');
      });

      return toupiaos;
    } else {
      throw new Error('获取投票列表失败');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

export async function getToupiao(toupiaoId, options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  info(`正在获取投票 ${toupiaoId} 的详情...`);

  const query = `
    query GetToupiaos($_id: ID) {
      toupiaos(_id: $_id, isRemove: false) {
        _id
        title
        content
        createdAt
        singleOption
        allowVoteCount
        voteTimeType
        allowUpdateVote
        publishResult
        endTime
        optionForms {
          title
          options {
            title
            isImage
            imageUrl
          }
          required
          minSelect
          maxSelect
        }
      }
    }
`;

  const variables = {
    _id: toupiaoId
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
        operationName: 'toupiaos'
      })
    );

    let toupiaos = null;
    if (Array.isArray(response.data)) {
      toupiaos = response.data;
    } else if (response.data && response.data.toupiaos) {
      toupiaos = response.data.toupiaos;
    }

    if (toupiaos && toupiaos.length > 0) {
      const toupiao = toupiaos[0];
      success('投票详情');
      log(colors.bright, `   ID: ${toupiao._id}`);
      log(colors.bright, `   标题: ${toupiao.title}`);
      if (toupiao.content)
        log(
          colors.cyan,
          `   描述: ${toupiao.content.substring(0, 100)}${toupiao.content.length > 100 ? '...' : ''}`
        );
      log(colors.cyan, `   类型: ${toupiao.singleOption ? '单选' : '多选'}`);
      if (toupiao.allowVoteCount)
        log(
          colors.cyan,
          `   投票次数限制: ${toupiao.voteTimeType || '总共'} ${toupiao.allowVoteCount}次`
        );
      if (toupiao.allowUpdateVote) log(colors.cyan, `   允许修改: 是`);
      if (toupiao.publishResult !== undefined)
        log(colors.cyan, `   公开结果: ${toupiao.publishResult ? '是' : '否'}`);
      if (toupiao.endTime)
        log(colors.cyan, `   结束时间: ${new Date(toupiao.endTime).toLocaleString('zh-CN')}`);
      if (toupiao.optionForms && toupiao.optionForms.length > 0) {
        log(colors.cyan, `   投票项 (${toupiao.optionForms.length} 个):`);
        toupiao.optionForms.forEach((form, index) => {
          log(colors.cyan, `     ${index + 1}. ${form.title} ${form.required ? '(必填)' : ''}`);
          if (form.options && form.options.length > 0) {
            form.options.forEach((opt, i) => {
              const imgStr = opt.isImage ? ' [图片]' : '';
              log(colors.cyan, `       ${String.fromCharCode(97 + i)}) ${opt.title}${imgStr}`);
            });
          }
        });
      }

      return toupiao;
    } else {
      throw new Error('未找到该投票');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

export async function updateToupiao(options) {
  const apiKey = getApiKey(options?.apiKey);

  if (!options.id) {
    error('请提供投票 ID (--id 参数)');
    process.exit(1);
  }

  const formConfig = {
    _id: options.id
  };

  if (options.title) formConfig.title = options.title;
  if (options.desc) formConfig.content = options.desc;
  if (options.single !== undefined) formConfig.singleOption = options.single === 'true' || options.single === '1';
  if (options.count) formConfig.count = parseInt(options.count);
  if (options.endTime) formConfig.endTime = new Date(options.endTime).getTime();
  if (options.publishResult !== undefined) formConfig.publishResult = options.publishResult === 'true' || options.publishResult === '1';
  if (options.anonymous !== undefined) formConfig.isAnonymous = options.anonymous === 'true' || options.anonymous === '1';
  if (options.allowVoteCount) formConfig.allowVoteCount = parseInt(options.allowVoteCount);
  if (options.minSelect) formConfig.minSelect = parseInt(options.minSelect);
  if (options.maxSelect) formConfig.maxSelect = parseInt(options.maxSelect);
  if (options.optionAllowOther !== undefined) formConfig.optionAllowOther = options.optionAllowOther === 'true' || options.optionAllowOther === '1';
  if (options.options) formConfig.optionForms = JSON.parse(options.options);

  info('正在更新投票...');

  const mutation = `
  mutation UpdateToupiao($input: updateToupiaoInput!) {
    updateToupiaoByInput(input: $input) {
      _id
      title
      content
      singleOption
      allowVoteCount
      publishResult
      isAnonymous
      endTime
      optionForms {
        title
        options {
          title
        }
      }
    }
  }
`;

  const data = JSON.stringify({
    query: mutation,
    variables: { input: formConfig },
    operationName: 'updateToupiaoByInput'
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

    const result = response.data.updateToupiaoByInput || response.data;
    if (result && result._id) {
      success('投票更新成功！');
      log(colors.bright, '   ID:', result._id);
      log(colors.bright, '   标题:', result.title);
      if (result.singleOption !== undefined) {
        log(colors.bright, '   类型:', result.singleOption ? '单选' : '多选');
      }
      if (result.publishResult !== undefined) {
        log(colors.bright, '   公开结果:', result.publishResult ? '是' : '否');
      }
      if (result.isAnonymous !== undefined) {
        log(colors.bright, '   匿名投票:', result.isAnonymous ? '是' : '否');
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

export async function getVotes(toupiaoId, options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  info(`正在获取投票 ${toupiaoId} 的结果...`);

  const toupiaoQuery = `
    query {
      toupiaos(_id: "${toupiaoId}", limit: "1") {
        _id
        title
        voteResults
        options
        allowVoteCount
        isMultiOptions
        optionForms {
          id
          title
          voteResults
        }
      }
    }
`;

  try {
    const toupiaoResponse = await httpsRequest(
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
        query: toupiaoQuery
      })
    );

    let toupiao = null;
    if (
      toupiaoResponse.data &&
      Array.isArray(toupiaoResponse.data) &&
      toupiaoResponse.data.length > 0
    ) {
      toupiao = toupiaoResponse.data[0];
    } else if (toupiaoResponse.data && toupiaoResponse.data.toupiao) {
      toupiao = toupiaoResponse.data.toupiao;
    }

    if (!toupiao) {
      throw new Error('获取投票结果失败');
    }

    success(`投票详情`);
    log(colors.bright, `   ID: ${toupiao._id}`);
    log(colors.bright, `   标题: ${toupiao.title}`);

    if (toupiao.isMultiOptions && toupiao.optionForms) {
      log(colors.cyan, `   投票项结果:`);
      toupiao.optionForms.forEach((form, index) => {
        const count = form.voteResults || 0;
        log(colors.cyan, `     ${index + 1}. ${form.title}: ${count} 票`);
      });
    } else if (toupiao.voteResults && Array.isArray(toupiao.voteResults)) {
      log(colors.cyan, `   投票结果:`);
      toupiao.options.forEach((opt, index) => {
        const count = toupiao.voteResults[index] || 0;
        log(colors.cyan, `     ${index + 1}. ${opt}: ${count} 票`);
      });
    }

    return { toupiao };
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}
