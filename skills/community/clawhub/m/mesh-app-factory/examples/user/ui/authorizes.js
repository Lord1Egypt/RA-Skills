import CfgSettings from "/assets/v3/settings/config.js";

export default {
components:{
    "cfgsettings":CfgSettings
},
inject:['service', 'tags'],
data() {return {
    curService:'',
    page:{cur:1, max:0},
    serviceOpts:[],
    users:[],
    roles:[],
    roleNames:{},
    cfg:{dlg:false,val:{},item:'',chged:false},
    newUser:{uids:[],service:'',role:'',power:[false],dlg:false},
    confirmDlg:null,
    alertDlg:null
}},
created(){
    this.service.get_services().then(resp => {
        if(resp['code']) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.serviceOpts=resp.options;

        var first=this.serviceOpts[0].value;
        this.curService=this.service.getRt("service", first);
        this.service.setRt("service", this.curService);

        this.cfg.item="ext_tmpl_"+this.curService;

        this.service.get_roles(this.curService).then(r => {
            if(r['code']&&r.code!=RetCode.OK) {
                this.$refs.errMsg.showErr(r.code, r.info);
                return;
            }
            this.roles=r.options;
            this.roleNames=r.names;
            this.list_users(1);
        })
    })
},
mounted(){//不能在created中赋值，更不能在data中
    this.confirmDlg=this.$refs.confirmDlg;
    this.alertDlg=this.$refs.errMsg;
},
methods:{
fmt_users(rows, cols) {
    var users=[];
    var sTypes=this.tags.user.statusTypes;
    for(var row of rows) { //id,account,nickName,ustatus,role
        var r={};
        for(var i in cols) {
            r[cols[i]]=row[i];
        }
        r.p=this.tags.user.powerNull;
        if(r.power && r.power.length>=2) {
            var t=JStr.base64CharCode(r.power.charAt(0));
            var v=JStr.base64CharCode(r.power.charAt(1));
            if(t == 0 && v == 1) { //当前只有一个权限
                r.p=this.tags.power.pubAccess;
            }
        }
        r.ustatus=sTypes[r.ustatus];
        users.push(r);
    }
    this.users=users;
},
list_users(pg){//查询服务用户极其角色
    var num=this.service.N_PAGE;
    var offset=(pg-1)*num;
    var url="/power/list?offset="+offset+"&num="+num+"&service="+this.curService;
    request({method:"GET",url:url},this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.users=[];
            return;
        }
        this.fmt_users(resp.data.users, resp.data.cols);
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
search_users() {
    if(this.search=='') {
        this.list_custs(1);
        return;
    }
    var url="/power/search?s="+this.search+"&limit="+this.service.N_PAGE+"&service="+this.curService;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.users=[];
            return;
        }
        this.fmt_users(resp.data.users, resp.data.cols);
        this.page.max=1;
    })
},
add_user() {
    var n=this.newUser;
    var p=JStr.base64Char(0) + JStr.base64Char(n.power[0]?1:0);
    var dta={uids:n.uids,service:this.curService,role:n.role,power:p};
    var opts={method:"POST",url:"/api/power/set",data:dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.newUser={dlg:false,uids:[],service:'',role:'',power:[false]};
        this.list_users(1);
    })
},
onServiceChange(s) {
    this.service.setRt("service", this.curService);
    this.service.get_roles(s).then(resp=>{
        if(resp['code']) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.roles=resp.options;
        this.roleNames=resp.names;
        this.cfg.item="ext_tmpl_"+this.curService;
        this.list_users(1);
    })
},
show_user(id) {
    this.service.jumpTo('/user?id='+id+"&app=" + this.curService);
},
save_cfg(){
    this.$refs.cfgSet.save().then(r=>{
        this.cfg.chged=!r;
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header elevated>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
     <q-toolbar-title>{{tags.authorize}}</q-toolbar-title>
     <q-select v-model="curService" :options="serviceOpts"
      emit-value map-options dark
      @update:model-value="onServiceChange">
      <template v-slot:selected-item="scope">
       <span class="text-white">{{scope.opt.label}}</span>
      </template>
     </q-select>
     <q-btn flat icon="settings_ethernet" @click="cfg.dlg=true">
      <q-badge color="orange" floating>{{tags.tmplDef}}</q-badge>
     </q-btn>
   </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="search" :label="tags.search" dense @keyup.enter="search_users">
     <template v-slot:append>
      <q-icon v-if="search!==''" name="close" @click="list_users(1)" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="search_users"></q-icon>
     </template>
     <template v-slot:after>
      <q-btn round color="primary" icon="add_circle" @click="newUser.dlg=true"></q-btn>
     </template>
    </q-input>
  </q-footer>
  
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
 <q-pagination v-model="page.cur" color="primary" :max="page.max" max-pages="10"
  boundary-numbers="false" @update:model-value="list_users"></q-pagination>
</div>
<q-list>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.user.account}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.power.role}}</q-item-label></q-item-section>
  <q-item-section side><q-item-label caption>{{tags.power.ext}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="u in users" clickable @click="show_user(u.id)">
  <q-item-section>
   <q-item-label>{{u.account}}({{u.ustatus}})</q-item-label>
   <q-item-label caption>{{u.nickName}}</q-item-label>
  </q-item-section>
  <q-item-section>{{roleNames[u.role]}}</q-item-section>
  <q-item-section side>{{u.p}}</q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="newUser.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.setPower}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-list dense>
    <q-item><q-item-section>
     <component-user-selector :label="tags.user.account" :accounts="newUser.uids" useid="true"></component-user-selector>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-select :label="tags.power.role" v-model="newUser.role" :options="roles" emit-value map-options></q-select>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-checkbox v-model="newUser.power[0]" :label="tags.power.pubAccess"></q-checkbox>
    </q-item-section></q-item>
   </q-list>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn :label="tags.ok" color="primary" @click="add_user"></q-btn>
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="cfg.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.tmplDef}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <cfgsettings v-model="cfg.val" ref="cfgSet" class="q-pa-md"
   :confirmDlg="confirmDlg" :alertDlg="alertDlg" :item="cfg.item"
   :service="service.name" :cfgTags="tags.cfgTags"
   @update:modelValue="cfg.chged=true" :showMap="false"></cfgsettings>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn :label="tags.save" color="primary" @click="save_cfg"
    :disable="!cfg.chged"></q-btn>
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
<component-confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></component-confirm-dialog>

`
}