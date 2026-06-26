import axios from 'axios';
import https from 'https';
export class LogEaseClient {
    client;
    constructor(config) {
        this.client = axios.create({
            baseURL: config.baseURL,
            headers: config.headers,
            httpsAgent: config.httpsAgent || new https.Agent({ rejectUnauthorized: false })
        });
    }
    /**
     * 执行GET请求
     */
    async get(path, params, options) {
        try {
            const response = await this.client.get(path, { params, ...options });
            return {
                status: response.status,
                data: response.data,
                message: '请求成功'
            };
        }
        catch (error) {
            return {
                status: error.response?.status || 500,
                error: error.message,
                details: error.response?.data,
                message: `请求失败: ${error.message}`
            };
        }
    }
    /**
     * 执行POST请求
     */
    async post(path, data, params) {
        try {
            const response = await this.client.post(path, data, { params });
            return {
                status: response.status,
                data: response.data,
                message: '请求成功'
            };
        }
        catch (error) {
            return {
                status: error.response?.status || 500,
                error: error.message,
                details: error.response?.data,
                message: `请求失败: ${error.message}`
            };
        }
    }
    /**
     * 执行PUT请求
     */
    async put(path, data, params) {
        try {
            const response = await this.client.put(path, data, { params });
            return {
                status: response.status,
                data: response.data,
                message: '请求成功'
            };
        }
        catch (error) {
            return {
                status: error.response?.status || 500,
                error: error.message,
                details: error.response?.data,
                message: `请求失败: ${error.message}`
            };
        }
    }
    /**
     * 执行DELETE请求
     */
    async delete(path, params) {
        try {
            const response = await this.client.delete(path, { params });
            return {
                status: response.status,
                data: response.data,
                message: '请求成功'
            };
        }
        catch (error) {
            return {
                status: error.response?.status || 500,
                error: error.message,
                details: error.response?.data,
                message: `请求失败: ${error.message}`
            };
        }
    }
    /**
     * 轮询请求直到完成或超时
     */
    async pollUntilComplete(path, checkComplete, maxRetries = 10, retryInterval = 5000, params, options) {
        let retries = 0;
        while (retries < maxRetries) {
            const result = await this.get(path, params, options);
            if (checkComplete(result)) {
                return result;
            }
            if (result.error) {
                return result;
            }
            await new Promise(resolve => setTimeout(resolve, retryInterval));
            retries++;
        }
        return {
            error: '轮询超时',
            message: `超过最大重试次数 (${maxRetries})`
        };
    }
}
