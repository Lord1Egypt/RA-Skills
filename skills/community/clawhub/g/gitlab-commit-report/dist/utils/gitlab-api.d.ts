import type { Page } from "puppeteer";
import type { CommitEvent } from "./storage.js";
interface GitLabConfig {
    gitlabUrl: string;
    groupId: string;
    groupName: string;
}
export declare function checkLogin(page: Page, gitlabUrl: string): Promise<void>;
export declare function fetchGroupPushEvents(page: Page, config: GitLabConfig, targetDate: string): Promise<CommitEvent[]>;
export {};
//# sourceMappingURL=gitlab-api.d.ts.map