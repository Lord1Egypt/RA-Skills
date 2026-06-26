const crypto = require('crypto');

class RTMClient {
    constructor(apiKey, sharedSecret) {
        this.apiKey = apiKey;
        this.sharedSecret = sharedSecret;
        this.endpoint = 'https://api.rememberthemilk.com/services/rest/';
        this.authEndpoint = 'https://www.rememberthemilk.com/services/auth/';
        this.token = null; // Will be set after auth
    }

    setToken(token) {
        this.token = token;
    }

    _signParams(params) {
        const keys = Object.keys(params).sort();
        let sigString = this.sharedSecret;
        for (const k of keys) {
            sigString += k + params[k];
        }
        return crypto.createHash('md5').update(sigString).digest('hex');
    }

    async callApi(method, params = {}) {
        const fullParams = {
            ...params,
            method,
            api_key: this.apiKey,
            format: 'json',
        };

        if (this.token && !fullParams.auth_token) {
            fullParams.auth_token = this.token;
        }

        fullParams.api_sig = this._signParams(fullParams);

        const qs = new URLSearchParams(fullParams).toString();
        const url = `${this.endpoint}?${qs}`;

        const res = await fetch(url);
        const data = await res.json();

        if (data.rsp.stat !== 'ok') {
            throw new Error(`RTM API Error: ${data.rsp.err.msg} (Code: ${data.rsp.err.code})`);
        }
        return data.rsp;
    }

    getAuthUrl() {
        const params = {
            api_key: this.apiKey,
            perms: 'delete' // read, write, or delete
        };
        params.api_sig = this._signParams(params);
        const qs = new URLSearchParams(params).toString();
        return `${this.authEndpoint}?${qs}`;
    }

    async getFrob() {
        const rsp = await this.callApi('rtm.auth.getFrob');
        return rsp.frob;
    }

    async getToken(frob) {
        const rsp = await this.callApi('rtm.auth.getToken', { frob });
        return rsp.auth.token;
    }

    async checkToken() {
        const rsp = await this.callApi('rtm.auth.checkToken');
        return rsp.auth;
    }

    async createTimeline() {
        const rsp = await this.callApi('rtm.timelines.create');
        return rsp.timeline;
    }

    async getLists() {
        const rsp = await this.callApi('rtm.lists.getList');
        return rsp.lists.list; // Array of list objects
    }

    async getTasks(filter = '') {
        const params = {};
        if (filter) params.filter = filter;
        const rsp = await this.callApi('rtm.tasks.getList', params);

        // Normalize return so it's always an array of tasks/series
        if (!rsp.tasks || !rsp.tasks.list) return [];

        let lists = Array.isArray(rsp.tasks.list) ? rsp.tasks.list : [rsp.tasks.list];
        let allTasks = [];

        for (const list of lists) {
            if (!list.taskseries) continue;
            let seriesArr = Array.isArray(list.taskseries) ? list.taskseries : [list.taskseries];
            for (const series of seriesArr) {
                // extract notes
                let notesArr = [];
                if (series.notes && series.notes.note) {
                    notesArr = Array.isArray(series.notes.note) ? series.notes.note : [series.notes.note];
                }

                let tasksArr = Array.isArray(series.task) ? series.task : [series.task];
                for (const task of tasksArr) {
                    allTasks.push({
                        list_id: list.id,
                        taskseries_id: series.id,
                        task_id: task.id,
                        name: series.name,
                        source: series.source,
                        priority: task.priority,
                        due: task.due,
                        completed: task.completed,
                        deleted: task.deleted,
                        tags: series.tags && series.tags.tag ? (Array.isArray(series.tags.tag) ? series.tags.tag : [series.tags.tag]) : [],
                        notes: notesArr
                    });
                }
            }
        }

        return allTasks;
    }

    async addTask(timeline, name, listId = null) {
        const params = { timeline, name };
        if (listId) params.list_id = listId;
        const rsp = await this.callApi('rtm.tasks.add', params);
        return rsp.list;
    }

    async completeTask(timeline, listId, taskseriesId, taskId) {
        const params = {
            timeline,
            list_id: listId,
            taskseries_id: taskseriesId,
            task_id: taskId
        };
        const rsp = await this.callApi('rtm.tasks.complete', params);
        return rsp.list;
    }

    async deleteTask(timeline, listId, taskseriesId, taskId) {
        const params = {
            timeline,
            list_id: listId,
            taskseries_id: taskseriesId,
            task_id: taskId
        };
        const rsp = await this.callApi('rtm.tasks.delete', params);
        return rsp.list;
    }

    async addNote(timeline, listId, taskseriesId, taskId, noteTitle, noteText) {
        const params = {
            timeline,
            list_id: listId,
            taskseries_id: taskseriesId,
            task_id: taskId,
            note_title: noteTitle,
            note_text: noteText
        };
        const rsp = await this.callApi('rtm.tasks.notes.add', params);
        return rsp.note;
    }

    async setDueDate(timeline, listId, taskseriesId, taskId, due) {
        const params = { timeline, list_id: listId, taskseries_id: taskseriesId, task_id: taskId, due, parse: '1' };
        const rsp = await this.callApi('rtm.tasks.setDueDate', params);
        return rsp.list;
    }

    async setStartDate(timeline, listId, taskseriesId, taskId, start) {
        const params = { timeline, list_id: listId, taskseries_id: taskseriesId, task_id: taskId, start, parse: '1' };
        const rsp = await this.callApi('rtm.tasks.setStartDate', params);
        return rsp.list;
    }

    async setPriority(timeline, listId, taskseriesId, taskId, priority) {
        const params = { timeline, list_id: listId, taskseries_id: taskseriesId, task_id: taskId, priority };
        const rsp = await this.callApi('rtm.tasks.setPriority', params);
        return rsp.list;
    }

    async postponeTask(timeline, listId, taskseriesId, taskId) {
        const params = { timeline, list_id: listId, taskseries_id: taskseriesId, task_id: taskId };
        const rsp = await this.callApi('rtm.tasks.postpone', params);
        return rsp.list;
    }
}

module.exports = RTMClient;
