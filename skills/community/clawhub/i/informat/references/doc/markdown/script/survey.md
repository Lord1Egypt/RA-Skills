# informat.survey Survey

## Overview

Use `informat.survey` to perform operations on the survey module.

## querySurveyListCount

Query the total count of surveys

```javascript
informat.survey.querySurveyListCount(moduleId, defineId, filter)
```

| Parameter       | Type                                      | Description      |
|----------|-----------------------------------------|---------|
| moduleId | `String`                                | Module identifier   |
| defineId | `String`                                | Survey identifier |
| filter   | [Filter](/guide/script/model.md#filter) | Filter criteria    |

Fields available in the filter

| Field              | Type        | Description     |
|-----------------|-----------|--------|
| id              | `String`  | Survey ID |
| name            | `String`  | Survey name |
| isEnable        | `Boolean` | Whether enabled   |
| submitCount     | `Integer` | Submission count   |
| createTime      | `String`  | Creation time   |
| createAccountId | `String`  | Creator ID  |

**Return Value**
Type is `Integer`
Returns the total count of surveys

**Example**

:::code-group

```js[Call]
informat.survey.querySurveyListCount('moduleId', 'defineId', {
    conditionList: [{
        fieldId: 'name',
        opt: 'eq',
        value: '织信NEXT问卷调查'
    }]
})
```

```json[Return Value]
1
```

:::

## querySurveyList

Query survey list

```javascript
informat.survey.querySurveyList(moduleId, defineId, query)
```

| Parameter       | Type                                    | Description      |
|----------|---------------------------------------|---------|
| moduleId | `String`                              | Module identifier   |
| defineId | `String`                              | Survey identifier |
| query    | [Query](/guide/script/model.md#query) | Query criteria    |

Fields available in the filter

| Field              | Type        | Description     |
|-----------------|-----------|--------|
| id              | `String`  | Survey ID |
| name            | `String`  | Survey name |
| isEnable        | `Boolean` | Whether enabled   |
| submitCount     | `Integer` | Submission count   |
| createTime      | `String`  | Creation time   |
| createAccountId | `String`  | Creator ID  |

**Return Value**
Type is Array<[SurveyItem](/guide/script/model.md#surveyitem)>
Returns the survey list

**Example**

:::code-group

```js[Call]
informat.survey.querySurveyList('moduleId', 'defineId', {
    pageIndex: 1,
    pageSize: 20,
    filter: {
        conditionList: [{
            fieldId: 'name',
            opt: 'eq',
            value: '织信NEXT问卷调查'
        }]
    }
});
```

:::

## addSurvey

Add a survey

```javascript
informat.survey.addSurvey(moduleId, defineId, survey)
```

| Parameter       | Type                                              | Description      |
|----------|-------------------------------------------------|---------|
| moduleId | `String`                                        | Module identifier   |
| defineId | `String`                                        | Survey identifier |
| survey   | [SurveyItem](/guide/script/model.md#surveyitem) | Survey information  |

**Return Value**
Type is `String`
Returns the newly created ID

**Example**

````javascript
const name = '调查问卷名称';
const value1 = '123456';
const value2 = 'abc';
const surveyInfo = {
    name: name,
    fieldList: [
        {
            id: "field1",
            value: value1,
        },
        {
            id: "field2",
            value: value2
        },
    ]
}
informat.survey.addSurvey('moduleId', 'defineId', surveyInfo);

````

## updateSurvey

Update survey information

```javascript
informat.system.updateSurvey(moduleId, defineId, survey, filter)
```

| Parameter       | Type                                              | Description      |
|----------|-------------------------------------------------|---------|
| moduleId | `String`                                        | Module identifier   |
| defineId | `String`                                        | Survey identifier |
| survey   | [SurveyItem](/guide/script/model.md#surveyitem) | Survey information  |
| filter   | [Filter](/guide/script/model.md#filter)         | Query criteria    |

Fields that can be updated

| Field              | Type                                                       | Description     |
|-----------------|----------------------------------------------------------|--------|
| name            | `String`                                                 | Name     |
| updateAccountId | `String`                                                 | Updater ID  |
| startTime       | `Date`                                                   | Start time   |
| endTime         | `Date`                                                   | End time   |
| fieldList       | Array<[SurveyField](/guide/script/model.md#surveyfield)> | Default field collection |
| isEnable        | `Boolean`                                                | Whether enabled   |
| rowNumber       | `Integer`                                                | Row position    |

**Return Value**
Type is `Integer`
Returns the total count of updates

**Example**

:::code-group

```js[Call]
const name = '问卷调查名称';
const surveyInfo = {
    name: name,
    fieldList:[
        {
            id: 'name',
            value: '张三',
        },
        {
            id: "age",
            value: 18
        },
    ]
}
informat.survey.updateSurvey('moduleId', 'defineId', surveyInfo, {
    conditionList:[{fieldId: 'name',opt:'eq', value: '调查问卷名称'}]
});
```

```json[Return Value]
1
```

:::

## deleteSurvey

Delete survey information

```javascript
informat.survey.deleteSurvey(moduleId, defineId, filter)
```

| Parameter       | Type                                      | Description      |
|----------|-----------------------------------------|---------|
| moduleId | `String`                                | Module identifier   |
| defineId | `String`                                | Survey identifier |
| filter   | [Filter](/guide/script/model.md#filter) | Query criteria    |

Fields available for filtering

| Field   | Type       | Description |
|------|----------|----|
| name | `String` | Name |

**Example**

:::code-group

```js[Call]
informat.survey.deleteSurvey('moduleId', 'defineId', {
    conditionList:[{fieldId: 'name',opt:'eq', value: '问卷调查名称'}]
})
```

```json[Return Value]
1
```

:::
