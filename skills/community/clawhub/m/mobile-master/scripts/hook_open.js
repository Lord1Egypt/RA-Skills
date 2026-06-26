function my_hook_dlopen(soName = '') {
    Interceptor.attach(Module.findExportByName(null, "android_dlopen_ext"),
        {
            onEnter: function (args) {
                var pathptr = args[0];
                if (pathptr !== undefined && pathptr != null) {
                    var path = ptr(pathptr).readCString();
                    if (path.indexOf(soName) >= 0) {
                        this.is_can_hook = true;
                    }
                }
            },
            onLeave: function (retval) {
                if (this.is_can_hook) {
                    hook_open();
                }
            }
        }
    );
}
function hook_open(){
    var pth = Module.findExportByName(null,"open");
  Interceptor.attach(ptr(pth),{
      onEnter:function(args){
          this.filename = args[0];
          console.log("",this.filename.readCString())
      },onLeave:function(retval){
      }
  })
}
setImmediate(my_hook_dlopen,"libjiagu_vip_64");