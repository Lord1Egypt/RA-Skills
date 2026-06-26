import { parseArgs, showHelp, loadConfig, mergeOptions } from './utils.js';
import { createTongji } from './commands/create.js';
import { updateTongji } from './commands/update.js';
import { listTongjis, getTongji, getBaomingsTotals, getBaomings } from './commands/list.js';
import { createToupiao, listToupiaos, getToupiao, getVotes, updateToupiao } from './commands/vote.js';
import { createBooking } from './commands/book.js';
import { createExam } from './commands/exam.js';
import { listChachas, getChacha, updateChacha } from './commands/chacha.js';
import { generateQrCode, generateToupiaoQrCode } from './commands/qrcode.js';
import { exportData } from './commands/export.js';
import { downloadFile, downloadFiles } from './commands/download.js';
import { login, logout } from './commands/login.js';

export {
  parseArgs,
  showHelp,
  createTongji,
  updateTongji,
  listTongjis,
  getTongji,
  getBaomingsTotals,
  getBaomings,
  createToupiao,
  updateToupiao,
  listToupiaos,
  getToupiao,
  getVotes,
  createBooking,
  createExam,
  listChachas,
  updateChacha,
  getChacha,
  generateQrCode,
  generateToupiaoQrCode,
  exportData,
  downloadFile,
  downloadFiles,
  login,
  logout
};

export async function main() {
  const args = process.argv.slice(2);
  const parsedArgs = parseArgs(args);
  const { command, options } = parsedArgs;

  if (options.config) {
    const configOptions = loadConfig(options.config);
    Object.assign(options, mergeOptions(options, configOptions));
  }

  if (!command || command === 'help' || options.help) {
    showHelp();
    return;
  }

  switch (command) {
    case 'create':
      if (!options.title) {
        console.error('--title 参数是必需的');
        process.exit(1);
      }
      await createTongji(options);
      break;

    case 'update':
      if (!options.id) {
        console.error('--id 参数是必需的');
        process.exit(1);
      }
      await updateTongji(options);
      break;

    case 'list':
      await listTongjis(options);
      break;

    case 'get':
      if (parsedArgs.args.length === 0) {
        console.error('请提供统计 ID');
        console.log('使用方法: miaoying get <tongji-id>');
        process.exit(1);
      }
      await getTongji(parsedArgs.args[0], options);
      break;

    case 'qrcode':
      if (parsedArgs.args.length === 0) {
        console.error('请提供实体 ID');
        console.log(
          '使用方法: miaoying qrcode <entity-id> [--type <tongji|booking|toupiao|chacha>]'
        );
        process.exit(1);
      }
      const entityTypeMap = {
        tongji: 'Tongji',
        booking: 'Booking',
        toupiao: 'Toupiao',
        chacha: 'Chacha',
        vote: 'Toupiao',
        exam: 'Tongji'
      };
      const entityType = options.type ? entityTypeMap[options.type] || 'Tongji' : 'Tongji';
      await generateQrCode(parsedArgs.args[0], { ...options, entityType });
      break;

    case 'totals':
      if (parsedArgs.args.length === 0) {
        console.error('请提供统计 ID');
        console.log('使用方法: miaoying totals <tongji-id>');
        process.exit(1);
      }
      await getBaomingsTotals(parsedArgs.args[0], options);
      break;

    case 'results':
      if (parsedArgs.args.length === 0) {
        console.error('请提供统计 ID');
        console.log('使用方法: miaoying results <tongji-id>');
        process.exit(1);
      }
      await getBaomings(parsedArgs.args[0], options);
      break;

    case 'vote':
    case 'create-vote':
      if (!options.title) {
        console.error('--title 参数是必需的');
        process.exit(1);
      }
      await createToupiao(options);
      break;

    case 'vote-list':
    case 'list-votes':
      await listToupiaos(options);
      break;

    case 'vote-get':
    case 'get-vote':
      if (parsedArgs.args.length === 0) {
        console.error('请提供投票 ID');
        console.log('使用方法: miaoying vote-get <toupiao-id>');
        process.exit(1);
      }
      await getToupiao(parsedArgs.args[0], options);
      break;

    case 'vote-results':
      if (parsedArgs.args.length === 0) {
        console.error('请提供投票 ID');
        console.log('使用方法: miaoying vote-results <toupiao-id>');
        process.exit(1);
      }
      await getVotes(parsedArgs.args[0], options);
      break;

    case 'update-vote':
      if (!options.id) {
        console.error('--id 参数是必需的');
        process.exit(1);
      }
      await updateToupiao(options);
      break;

    case 'vote-qrcode':
      if (parsedArgs.args.length === 0) {
        console.error('请提供投票 ID');
        console.log('使用方法: miaoying vote-qrcode <toupiao-id>');
        process.exit(1);
      }
      await generateToupiaoQrCode(parsedArgs.args[0], options);
      break;

    case 'book':
    case 'booking':
    case 'create-book':
      if (!options.title) {
        console.error('--title 参数是必需的');
        process.exit(1);
      }
      await createBooking(options);
      break;

    case 'exam':
    case 'create-exam':
      if (!options.title) {
        console.error('--title 参数是必需的');
        process.exit(1);
      }
      await createExam(options);
      break;

    case 'chacha':
    case 'chacha-list':
    case 'list-chachas':
      await listChachas(options);
      break;

    case 'chacha-get':
    case 'get-chacha':
      if (parsedArgs.args.length === 0) {
        console.error('请提供查查 ID');
        console.log('使用方法: miaoying chacha-get <chacha-id>');
        process.exit(1);
      }
      await getChacha(parsedArgs.args[0], options);
      break;

    case 'update-chacha':
      if (!options.id) {
        console.error('--id 参数是必需的');
        process.exit(1);
      }
      await updateChacha(options);
      break;

    case 'export':
    case 'export-data':
      if (parsedArgs.args.length === 0) {
        console.error('请提供活动 ID');
        console.log(
          '使用方法: miaoying export <activity-id> --type <tongji|booking|toupiao|chacha>'
        );
        process.exit(1);
      }
      await exportData(parsedArgs.args[0], options);
      break;

    case 'upload':
      // 上传功能已移除 - 引导用户到秒应小程序编辑
      console.log('📷 文件上传功能已移至秒应小程序');
      console.log('');
      console.log('请按以下步骤操作：');
      console.log('  1. 打开微信，搜索"秒应"小程序，注意蓝绿小人那个Logo才是正版');
      console.log('  2. 进入对应的统计/投票/预约活动');
      console.log('  3. 在编辑页面中上传图片或文件');
      console.log('');
      console.log('如需帮助，请联系技术支持');
      break;

    case 'login':
      await login(options);
      break;

    case 'logout':
      await logout();
      break;

    case 'download':
      if (parsedArgs.args.length === 0) {
        console.error('请提供要下载的文件 URL');
        console.log('使用方法: miaoying download <file-url> [--entity <type>][--verbose]');
        process.exit(1);
      }
      await downloadFile(parsedArgs.args[0], { ...options, useThumbnail: !options.original });
      break;

    default:
      console.error('未知命令:', command);
      console.log('使用 "miaoying help" 查看帮助');
      process.exit(1);
  }
}
