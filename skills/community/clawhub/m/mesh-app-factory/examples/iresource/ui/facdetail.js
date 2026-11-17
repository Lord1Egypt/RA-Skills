import SupplierInput from "./components/supplier_selector.js";
export default {
inject:['service', 'tags'],
components:{
    "supplier-input":SupplierInput
},
data() {return {
    id:this.$route.query.id,
    facInfo:{}, //工厂信息
    admins:[], //管理员
    ctrl:{fun:'',dta:{},admTypes:[]},
    edtAdm:{show:false,type:'',account:''}
}},
created(){
    this.get();
    this.getAdmins();
    for(var i in this.tags.admType) {
        this.ctrl.admTypes.push({label:this.tags.admType[i],value:i});
    }
},
methods:{
get() {
    var url = "/api/factory/get?id="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var dt=new Date();
        dt.setTime(resp.data.createAt*60000);
        resp.data.createAt_s=date2str(dt);
        this.facInfo=resp.data;
    })
},
update() {
    var opts={method:"PUT",url:"/factory/update",data:this.ctrl.dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        copyObjTo(this.ctrl.dta, this.facInfo);
        this.ctrl.fun='';
    });
},
remove() {
    var opts={method:"DELETE",url:"/factory/remove?id="+this.id};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.service.back();
    });
},
show_edit() {
    copyObjTo(this.facInfo, this.ctrl.dta);
    this.ctrl.dta.id=this.id;
    this.ctrl.fun='edit';
},
//管理员记录操作
getAdmins() {
    var url = "/api/factory/listAdmin?factory="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.admins=[];
            return;
        }
        for(var l of resp.data.list) {
            l.type_s=this.tags.admType[l.type];
        }
        this.admins=resp.data.list;
    });
},
showAddAdm() {
    this.edtAdm.type='';
    this.edtAdm.account=[];
    this.edtAdm.show=true;
},
addAdmin() {
    if(this.edtAdm.account.length<1){
        this.$refs.errMsg.showErr(RetCode.WRONG_PARAMETER, "invalid account");
        return;
    }
    var url = "/api/factory/addAdmin";
    var dta={factory:this.id,account:this.edtAdm.account[0],type:this.edtAdm.type};
    request({method:"POST",url:url,data:dta}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        dta.type_s=this.tags.admType[dta.type];
        this.admins.push(dta);
        this.edtAdm.show=false;
    });
},
removeAdmin(i) {
    var url = "/api/factory/removeAdmin?factory="+this.id
        +"&account="+this.admins[i].account;
    request({method:"DELETE",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.admins.splice(i,1);
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.detail}}-{{facInfo.name}}</q-toolbar-title>
    <q-btn icon="delete_forever" @click="remove" flat dense></q-btn>
    <q-btn icon="edit" @click="show_edit" flat dense></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<div v-if="ctrl.fun==''">
 <q-list dense>
  <q-item>
   <q-item-section>{{tags.name}}</q-item-section>
   <q-item-section>{{facInfo.name}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.factory.addr}}</q-item-section>
   <q-item-section>{{facInfo.addr}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.cmt}}</q-item-section>
   <q-item-section>{{facInfo.cmt}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.createAt}}</q-item-section>
   <q-item-section>{{facInfo.createAt_s}}</q-item-section>
  </q-item>
 </q-list>
</div>
<div v-else>
 <q-list dense>
  <q-item>
   <q-item-section>{{tags.name}}</q-item-section>
   <q-item-section><q-input v-model="ctrl.dta.name" dense></q-input></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.factory.addr}}</q-item-section>
   <q-item-section><q-input v-model="ctrl.dta.addr" dense></q-input></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.cmt}}</q-item-section>
   <q-item-section><q-input v-model="ctrl.dta.cmt" dense></q-input></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.createAt}}</q-item-section>
   <q-item-section>{{facInfo.createAt_s}}</q-item-section>
  </q-item>
 </q-list>
 <div class="text-right">
  <q-btn flat :label="tags.cancel" color="primary" @click="ctrl.fun=''"></q-btn>
  <q-btn icon="done" :label="tags.ok" color="primary" @click="update"></q-btn>
 </div>
</div>
<q-separator inset></q-separator>
<q-banner inline-actions class="bg-indigo-1 q-ma-sm" dense>
  {{tags.factory.admin}}
  <template v-slot:action>
   <q-icon flat color="primary" name="add_circle" @click.stop="showAddAdm"></q-icon>
  </template>
</q-banner>
<q-list dense>
  <q-item v-for="(a,i) in admins">
   <q-item-section>{{a.account}}</q-item-section>
   <q-item-section>{{a.type_s}}</q-item-section>
   <q-item-section side>
    <q-btn icon="cancel" color="red" @click="removeAdmin(i)" flat></q-btn>
   </q-item-section>
  </q-item>
  <q-item v-show="edtAdm.show">
   <q-item-section>
    <user-selector :label="tags.factory.account" :accounts="edtAdm.account"></user-selector>
   </q-item-section>
   <q-item-section>
    <q-select v-model="edtAdm.type" :options="ctrl.admTypes" emit-value map-options></q-select>
   </q-item-section>
   <q-item-section side>
   <q-btn :label="tags.ok" color="primary" @click="addAdmin" flat></q-btn>
    <q-btn :label="tags.cancel" color="primary" @click="edtAdm.show=false" flat></q-btn>
   </q-item-section>
  </q-item>
</q-list>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}