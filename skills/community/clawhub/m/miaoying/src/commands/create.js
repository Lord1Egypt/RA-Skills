import { getApiKey, httpsRequest, API_HOST, log, colors, success, error, info, safeJsonParse } from '../utils.js';

export async function createTongji(options) {
  const apiKey = getApiKey(options?.apiKey);

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
    title: options.title || '未命名统计',
    content: options.desc || '',
    infoForms: parsedForms
  };

  if (options.count) formConfig.count = parseInt(options.count);
  if (options.endTime) formConfig.endTime = new Date(options.endTime).getTime();
  if (options.anonymous) formConfig.isAnonymous = true;

  info('正在创建统计...');

  const mutation = `
  mutation CreateTongji($input: TongjiInput!) {
    createTongjiByInput(input: $input) {
      _id
      title
      createdAt
      infoForms {
        title
        type
        required
      }
    }
  }
`;

  const data = JSON.stringify({
    query: mutation,
    variables: { input: formConfig },
    operationName: 'createTongjiByInput'
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

    if (response.data && response.data._id) {
      success('统计创建成功！');
      log(colors.bright, '   ID:', response.data._id);
      log(colors.bright, '   标题:', response.data.title);
      log(colors.bright, '   字段数:', response.data.infoForms?.length || 0);

      if (options.qrcode) {
        info('正在生成二维码...');
        const { generateQrCode } = await import('./qrcode.js');
        await generateQrCode(response.data._id, options);
      } else {
        info('使用以下命令生成二维码:');
        log(colors.cyan, `   miaoying qrcode ${response.data._id}`);
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
