Interceptor.attach(Module.findExportByName(null, "android_dlopen_ext"), {

    onEnter: function (args) {

        console.log("加载SO：" + args[0].readCString() );

    }

});

console.log("监控启动！操作APP看SO加载路径～");