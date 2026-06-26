# Lynse CLI 兼容性对照表

## 📋 命令映射关系

### 基础认证命令（双向兼容）
| 命令 | CLI A 支持 | CLI B 支持 | 备注 |
|------|------------|------------|------|
| `bind` | ✅ | ✅ | |
| `exchangeToken` | ✅ | ✅ | CLI B 中有增强实现 |
| `generateApiKey` | ✅ | ✅ | |
| `isLogin` | ✅ | ✅ | |
| `login` | ✅ | ✅ | CLI B 支持更多登录方式 |
| `logout` | ✅ | ✅ | |
| `refreshToken` | ✅ | ✅ | |
| `register` | ✅ | ✅ | CLI B 支持更多注册选项 |
| `render` | ✅ | ✅ | |
| `revokeApiKey` | ✅ | ✅ | |
| `terminate` | ✅ | ✅ | |
| `updatePhone` | ✅ | ✅ | |
| `updatePwd` | ✅ | ✅ | |
| `verifyWechatSignature` | ✅ | ✅ | |
| `getPoolStatus` | ✅ | ✅ | |
| `smsCode` | ✅ | ✅ | |

### CLI B 新增高级命令
| 命令分类 | 新增命令 |
|----------|----------|
| **用户管理** | `claim`, `claimByActivityId`, `list4`, `chatStream`, `listChatFiles`, `bindVocabulary`, `getBoundVocabulary`, `listEnabledVocabularies`, `unbindVocabulary`, `auditText`, `list3`, `changeTeam`, `current`, `detail`, `edit2`, `edit3`, `grantMonthlyReward`, `grantTeamUpgrade`, `list2`, `outPutLanguage`, `recharge1` |
| **设备管理** | `isBound`, `listMyBindingDeviceList`, `unbind`, `update`, `updateConnectTime` |
| **文件处理** | `addEvaluation`, `changeFolder`, `cleanBin`, `cleanBinAll`, `countByCategory`, `delete`, `edit`, `getAvailableAIModelList`, `getEvaluationList`, `getStsToken`, `getSupportLanguage`, `handleAudioMergeCallback`, `info1`, `list`, `listByCategory`, `listByCategoryV1`, `listByTimeRange`, `markFileAsRead`, `notify`, `page`, `pageByCategory`, `presign4Download`, `presign4Upload`, `presign4UploadForPublic`, `queryAudioMergeStatus`, `recover`, `removeOss`, `submitAudioMerge`, `testAudioMerge`, `aiModelProcessText`, `batchGetConclusions`, `deleteConclusion`, `editConclusion`, `editMindMap`, `editOutline`, `editSpeakerInfo`, `editTransRecord`, `exportHtmlToPdf`, `exportOutline`, `exportTransRecord`, `getAiTaskResult`, `getConclusion`, `getConclusionList`, `getMindMap`, `getOutline`, `getTranscribeStatus`, `handleTransCallback`, `listTranscriptionRecord`, `transferFile`, `updateFeedback` |
| **团队协作** | `createTeam`, `deleteTeam`, `editTeam`, `info`, `leaveTeam`, `listMyTeam`, `recharge`, `removeTeamMember`, `editTeamFile`, `getFileInfo`, `listTeamFile`, `moveOrCopy`, `removeTeamFile`, `createInvitation`, `handleInvite`, `listMyInvitation` |
| **推送服务** | `init`, `testAndroidPush`, `testIosPush` |
| **翻译服务** | `getLatestSpeakerNames`, `getPromptTemplateCategories`, `getRegenerateSelectList`, `getTranscriptionLanguageList`, `getTranslateHistory`, `getTranslateResult` |
| **其他功能** | `add`, `batchUpdateSort`, `edit1`, `list1`, `selectOne`, `checkApkUpdate`, `checkVersion`, `getFunctionList`, `presignUrl`, `queryPointsLog`, `generateShareLink`, `getSharedInfo`, `allocatePointsToTeam`, `assignRole`, `checkTeamAdminOrOwner` |

## 🚀 迁移建议

1. **逐步迁移策略**
   - 先统一使用 `lynse_unified.sh` 作为入口
   - 对于复杂功能，逐步迁移到CLI B的专属实现

2. **兼容层优势**
   - 自动检测可用的CLI版本
   - 对于不支持的命令给出清晰错误提示
   - 保留对旧版本的向下兼容

3. **推荐做法**
   - 新开发的功能优先使用CLI B的高级命令
   - 旧有代码可以继续使用，由统一层自动路由