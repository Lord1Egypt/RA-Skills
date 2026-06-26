// 插件元数据
const pluginMeta = {
  "name": "bilibili",
  "version": "1.0.0",
  "capabilities": [
    "advanced"
  ],
  "tier": "advanced",
  "supportedPlatforms": [
    "bilibili"
  ],
  "features": [
    "video-extraction",
    "subtitle-extraction",
    "video-info"
  ],
  "description": "B站视频内容提取",
  "dependencies": [
    "axios",
    "fluent-ffmpeg"
  ]
};

// B站内容获取插件
const fetch = require('node-fetch');

class Bilibili {
  constructor(options = {}) {
    this.supportedPlatforms = ["bilibili"];
    this.sesData = options.sesData; // B站登录凭证
    this.baseUrl = 'https://api.bilibili.com/x';
  }

  /**
   * 获取关注的UP主动态
   * @param {number} pageSize 页面大小
   */
  async getFollowingDynamics(pageSize = 20) {
    try {
      const url = `${this.baseUrl}/polymer/web-dynamic/v1/feed/all?type=all&page_size=${pageSize}`;
      const response = await fetch(url, {
        headers: {
          'Cookie': `SESSDATA=${this.sesData}`,
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
      });

      const data = await response.json();

      if (data.code !== 0) {
        throw new Error(data.message);
      }

      return data.data.items
        .filter(item => item.type === 'DYNAMIC_TYPE_AV') // 过滤视频动态
        .map(item => ({
          title: item.modules.module_dynamic.major.archive.title,
          description: item.modules.module_dynamic.major.archive.desc,
          url: `https://www.bilibili.com/video/${item.modules.module_dynamic.major.archive.bvid}`,
          cover: item.modules.module_dynamic.major.archive.cover,
          duration: item.modules.module_dynamic.major.archive.duration,
          author: item.modules.module_author.author.name,
          authorId: item.modules.module_author.author.mid,
          publishTime: new Date(item.modules.module_author.pub_time * 1000),
          tags: this.extractTags(item.modules.module_dynamic.major.archive),
          source: 'bilibili',
          type: 'video',
          stats: item.modules.module_dynamic.major.archive.stat // 点赞、播放等数据
        }));
    } catch (error) {
      console.error('获取B站动态失败:', error);
      return [];
    }
  }

  /**
   * 获取指定UP主的视频列表
   * @param {string} uid UP主UID
   * @param {number} pageSize 每页数量
   */
  async getUserVideos(uid, pageSize = 20) {
    try {
      const url = `${this.baseUrl}/space/arc/search?mid=${uid}&ps=${pageSize}&order=pubdate`;
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
      });

      const data = await response.json();

      if (data.code !== 0) {
        throw new Error(data.message);
      }

      return data.data.list.vlist.map(video => ({
        title: video.title,
        description: video.description,
        url: `https://www.bilibili.com/video/${video.bvid}`,
        cover: video.pic,
        duration: this.formatDuration(video.length),
        author: video.author,
        authorId: uid,
        publishTime: new Date(video.created * 1000),
        tags: video.tag?.split(',') || [],
        source: 'bilibili',
        type: 'video',
        stats: {
          play: video.play,
          danmaku: video.video_review
        }
      }));
    } catch (error) {
      console.error('获取UP主视频失败:', error);
      return [];
    }
  }

  /**
   * 获取视频详细信息
   * @param {string} bvid 视频BV号
   */
  async getVideoInfo(bvid) {
    try {
      const url = `${this.baseUrl}/web-interface/view?bvid=${bvid}`;
      const response = await fetch(url);

      const data = await response.json();

      if (data.code !== 0) {
        throw new Error(data.message);
      }

      const video = data.data;
      return {
        title: video.title,
        description: video.desc,
        url: `https://www.bilibili.com/video/${bvid}`,
        cover: video.pic,
        duration: this.formatDuration(video.duration),
        author: video.owner.name,
        authorId: video.owner.mid,
        publishTime: new Date(video.pubdate * 1000),
        tags: video.tags.map(tag => tag.tag_name),
        source: 'bilibili',
        type: 'video',
        stats: {
          view: video.stat.view,
          danmaku: video.stat.danmaku,
          reply: video.stat.reply,
          favorite: video.stat.favorite,
          coin: video.stat.coin,
          like: video.stat.like
        }
      };
    } catch (error) {
      console.error('获取视频信息失败:', error);
      return null;
    }
  }

  formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  }

  extractTags(archive) {
    // 从视频信息中提取标签
    return archive.tag?.split(',') || [];
  }
}

module.exports = Bilibili;