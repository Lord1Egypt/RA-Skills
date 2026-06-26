const axios = require('axios');

async function getModelList() {
    try {
        const response = await axios.get('https://cwork-api-test.xgjktech.com.cn/filegpt/t_ai/nologin/aiTypeList');
        return response.data;
    } catch (error) {
        console.error('Error fetching model list:', error);
        return { error: 'Failed to fetch model list' };
    }
}

module.exports = { getModelList };
