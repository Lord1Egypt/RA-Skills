export default {
inject:['service', 'tags'],
data() {return {
    users:[], //account,nickName,mobile
    page:{cur:1, max:0},
    search:'',
    newUser:{dlg:false,account:'',password:'',nickName:''}
}},
created(){
    this.list_users(1);
},
methods:{
fmt_users(rows, cols) {
    var types=this.tags.user.typeTitles;
    var sexs=this.tags.user.sexTitles;
    var sTypes=this.tags.user.statusTypes;
    var users=[];
    for(var row of rows) { //id,name,address,createAt,status,creator
        var r={};
        for(var i in cols) {
            r[cols[i]]=row[i];
        }
        r.type=types[r.type];
        r.sex=sexs[r.sex];
        r.sStatus=sTypes[r.ustatus];
        users.push(r);
    }
    this.users=users;
},
list_users(pg){
    var num=this.service.N_PAGE;
    var offset=(pg-1)*num;
    var url="/user/list?offset="+offset+"&num="+num;
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
    var url="/user/search?s="+this.search+"&limit="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.users=[];
            return;
        }
        this.fmt_users(resp.data.users, resp.data.cols);
        this.page.max=1;
    });
},
add_user() {
    var opts={method:"POST",url:"/api/user/add",data:this.newUser};
    request(opts, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.newUser={dlg:false,account:'',password:'',nickName:''};
        this.list_users(1);
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header elevated>
   <q-toolbar>
      <q-toolbar-title>{{tags.app_name}}</q-toolbar-title>
      <q-btn icon="fact_check" flat round @click="service.jumpTo('/authorizes')"></q-btn>
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
  <q-item-section><q-item-label caption>{{tags.user.nickName}}</q-item-label></q-item-section>
  <q-item-section side><q-item-label caption>{{tags.user.type}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="u in users" :class="u.ustatus=='N'?'':'bg-grey-1'" @click="service.jumpTo('/user?id='+u.id)" clickable>
  <q-item-section>{{u.account}}</q-item-section>
  <q-item-section>{{u.nickName}}({{u.sex}})</q-item-section>
  <q-item-section side>{{u.type}}({{u.sStatus}})</q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="newUser.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.newUser}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-list dense>
    <q-item>
     <q-item-section><q-input :label="tags.user.account" v-model="newUser.account" dense></q-input></q-item-section>
    </q-item>
    <q-item>
     <q-item-section><q-input :label="tags.user.nickName" v-model="newUser.nickName" dense></q-input></q-item-section>
    </q-item>
    <q-item>
     <q-item-section><q-input :label="tags.user.pwd" v-model="newUser.password" type="password" dense></q-input></q-item-section>
    </q-item>
   </q-list>
  </q-card-section>
  <q-card-actions align="right">
     <q-btn :label="tags.ok" color="primary" @click="add_user"></q-btn>
     <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}