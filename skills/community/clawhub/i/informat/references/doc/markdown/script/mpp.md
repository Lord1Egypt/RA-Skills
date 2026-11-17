# informat.mpp MPP File

## Overview

Use `informat.mpp` to perform read and write operations on MPP files

## createProjectFile

Create an MPP project file object

```javascript
informat.mpp.createProjectFile()
```

**Return Value**

Type is `MppProjectFile`

## read

Read an MPP file from the local sandbox. An exception will be thrown if the file does not exist

```javascript
informat.mpp.read(file)
```

| Parameter | Type   | Description                          |
|-----------|--------|--------------------------------------|
| file      | String | MPP file path in the app sandbox environment |

**Return Value**

Type is `MppProjectFile`

**Example**

```js
let projectFile = informat.mpp.read('software_development.mpp');
var resourceAssignments = projectFile.getResourceAssignments();
resourceAssignments.list().forEach(as => {
    if (as.getTask() == null || as.getResource() == null) {
        return;
    }
    var taskId = as.getTask().getID();
    var resourceName = as.getResource().getName();
    console.log('taskId:' + taskId + ',resourceName:' + resourceName);
});
var tableContainer = projectFile.getTables();
if (tableContainer != null && tableContainer.size() > 0) {
    var columns = tableContainer.list().get(0).getColumns();
    columns.forEach(c => {
        console.log('column:' + c.getTitle());
    });
}
var tasks = projectFile.getTasks();
tasks.list().forEach(task => {
    console.log('taskId:' + task.getID() + ',taskName:' + task.getName());
});
```

## write

Write projectFile data to an XML file

```js
informat.mpp.write(projectFile, targetFile, config)
```

| Parameter   | Type                                                      | Description                          |
|-------------|-----------------------------------------------------------|--------------------------------------|
| projectFile | `MppProjectFile`                                          | Project file object                  |
| targetFile  | `String`                                                  | File path in the app sandbox environment |
| config      | [MppWriterConfig](/guide/script/model.md#mppwriterconfig) | Configuration file                   |

```js
var file = informat.mpp.createProjectFile();
var pmResource = file.addResource();
pmResource.setName("Project Manager");
var devResource = file.addResource();
devResource.setName("Developer");
var customFieldContainer = file.getCustomFields();
var field = customFieldContainer.getOrCreate('TEXT1');
field.setAlias("MyCustomField");
var task1 = file.addTask();
task1.setName("root");
task1.setTaskMode('MANUALLY_SCHEDULED');
task1.setStart(new Date());
task1.setFinish(new Date(2024, 3, 1));
task1.setText(1, 'Test 1')
task1.addResourceAssignment(pmResource);
task1.addResourceAssignment(devResource);
//
var task12 = task1.addTask();
task12.setName("Task A");
task12.setTaskMode('AUTO_SCHEDULED');
task12.setStart(new Date());
task12.setFinish(new Date(2024, 2, 1));
task12.setText(1, "text1");
task12.addResourceAssignment(devResource);
//
task1.addPredecessor(task12, null, null);
task12.addPredecessor(task1, null, null);
//
var task2 = file.addTask();
task2.setName("Task B");
task2.setTaskMode('MANUALLY_SCHEDULED');
task2.setStart(new Date(2024, 4, 1));
task2.setFinish(new Date(2024, 5, 1));
//
var config = {
    microsoftProjectCompatibleOutput: false,
    splitTimephasedAsDays: true,
    writeTimephasedData: false,
    saveVersion: "Project2016"
}
informat.mpp.write(file, 'output.xml', config);
```

::: info Reference Documentation:
[https://www.mpxj.org/apidocs/index.html](https://www.mpxj.org/apidocs/index.html)
:::
