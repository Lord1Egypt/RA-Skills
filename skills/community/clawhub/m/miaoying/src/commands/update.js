import { getApiKey, httpsRequest, API_HOST, log, colors, success, error, info, loadConfig, safeJsonParse } from '../utils.js';

export async function updateTongji(options) {
  const apiKey = getApiKey(options?.apiKey);

  // 支持配置文件
  if (options.config) {
    const config = loadConfig(options.config);
    // CLI 参数覆盖配置文件
    options = { ...config, ...options };
  }

  if (!options.id) {
    error('请提供统计 ID (--id 参数)');
    process.exit(1);
  }

  let parsedForms = [];
  if (options.infoForms) {
    try {
      parsedForms = typeof options.infoForms === 'string'
        ? safeJsonParse(options.infoForms, 'info-forms')
        : options.infoForms;
    } catch (err) {
      error(`表单字段解析失败: ${err.message}`);
      info('请确保 --info-forms 参数是有效的 JSON 数组格式');
      process.exit(1);
    }
  }

  const formConfig = {
    _id: options.id
  };

  if (options.title) formConfig.title = options.title;
  if (options.desc) formConfig.content = options.desc;
  if (parsedForms.length > 0) formConfig.infoForms = parsedForms;
  if (options.count) formConfig.count = parseInt(options.count);
  if (options.endTime) formConfig.endTime = new Date(options.endTime).getTime();
  if (options.anonymous) formConfig.isAnonymous = true;
  if (options.close !== undefined) formConfig.isClose = options.close === 'true' || options.close === '1';
  if (options.repeat !== undefined) formConfig.isRepeat = options.repeat === 'true' || options.repeat === '1';

  // 支持通过配置文件传入更多参数（如 pictures, cover 等）
  if (options.pictures) formConfig.pictures = options.pictures;
  if (options.cover) formConfig.cover = options.cover;
  if (options.files) formConfig.files = options.files;
  if (options.videoArr) formConfig.videoArr = options.videoArr;

  info('正在更新统计...');

  const mutation = `
  mutation UpdateTongji($input: TongjiInput!) {
    updateTongjiByInput(input: $input) {
      _id
      title
      content
      pictures
      cover
      infoForms {
        title
        type
        required
        options
      }
      isClose
      isAnonymous
      isRepeat
    }
  }
`;

  const data = JSON.stringify({
    query: mutation,
    variables: { input: formConfig },
    operationName: 'updateTongjiByInput'
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

    const result = response.data.updateTongjiByInput || response.data;
    if (result && result._id) {
      success('统计更新成功！');
      log(colors.bright, '   ID:', result._id);
      log(colors.bright, '   标题:', result.title);
      if (result.pictures && result.pictures.length > 0) {
        log(colors.bright, '   图片数:', result.pictures.length);
      }
      if (result.cover) {
        log(colors.bright, '   封面:', result.cover);
      }
      if (result.infoForms?.length > 0) {
        log(colors.bright, '   表单字段:', result.infoForms.length);
      }
      if (result.isClose !== undefined) {
        log(colors.bright, '   已关闭:', result.isClose ? '是' : '否');
      }
      if (result.isAnonymous !== undefined) {
        log(colors.bright, '   匿名:', result.isAnonymous ? '是' : '否');
      }
      if (result.isRepeat !== undefined) {
        log(colors.bright, '   允许重复:', result.isRepeat ? '是' : '否');
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